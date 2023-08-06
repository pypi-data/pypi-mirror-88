# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List, Union, Tuple
import os, time
from urllib.parse import quote
from requests import Response

# Pip
from ksimpleapi import Api
from kcu import strio
from bs4 import BeautifulSoup as bs

# Local
from .models import *

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# --------------------------------------------------------- class: ProxiesDotCom --------------------------------------------------------- #

class ProxiesDotCom(Api):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        cache_folder_path: str,
        email: str,
        password: str,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        max_request_try_count: int = 1,
        sleep_s_between_failed_requests: Optional[float] = 0.5,
        debug: bool = False
    ):
        cache_folder_path = os.path.join(cache_folder_path, email)

        if not os.path.exists(cache_folder_path):
            os.makedirs(cache_folder_path)

        self.cookies_file_path = os.path.join(cache_folder_path, 'cookies.pkl')
        user_agent_file_path = os.path.join(cache_folder_path, 'user_agent.txt')

        cached_user_agent = strio.load(user_agent_file_path)

        if cached_user_agent:
            user_agent = cached_user_agent
        elif user_agent:
            strio.save(user_agent_file_path, user_agent)

        super().__init__(
            user_agent=user_agent,
            proxy=proxy,
            keep_cookies=True,
            cookies_file_path=self.cookies_file_path,
            max_request_try_count=max_request_try_count,
            sleep_s_between_failed_requests=sleep_s_between_failed_requests,
            allow_redirects=False,
            debug=debug
        )

        if not self.is_logged_in():
            if self.debug:
                print('Could not find usable cookies. Logging in.')

            if self.login(email, password, remember=True):
                if self.debug:
                    print('Successfullly logged in')
            elif self.debug:
                print('Could not log in')
        elif self.debug:
            print('Using cookies, no need to re-login')


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    def is_logged_in(self, url_verification_fallback: bool = True) -> bool:
        if not os.path.exists(self.cookies_file_path):
            return False

        if url_verification_fallback:
            try:
                return self._get('https://www.proxies.com/home').status_code == 200
            except:
                return False

        return True

    @classmethod
    def extra_headers(cls):
        return {
            'Host': 'www.proxies.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Origin': 'https://www.proxies.com'
        }

    def login(
        self,
        email: str,
        password: str,
        remember: bool = True
    ) -> bool:
        referer_url = 'https://www.proxies.com/login'
        token_res = self._get_resp_with_token(referer_url)

        if not token_res:
            return None

        _, token = token_res

        args = {
            '_token': token,
            'email': email,
            'password': password,
            'remember': 'on' if remember else None
        }

        parsed_args = '&'.join(['{}={}'.format(k, quote(v)) for k, v in args.items() if v])
        res = self._post('https://www.proxies.com/login', body=parsed_args, extra_headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': len(parsed_args),
            'Referer': referer_url
        })

        if not res:
            if self.debug:
                print('Something went wrong. Could not login')

            return False

        return res.status_code == 302
    
    def update_proxy_auth_settings(
        self,
        reference: str,
        proxy_name: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        authenticated_ips: Optional[List[str]] = None
    ) -> bool:
        referer_url = 'https://www.proxies.com/proxy/{}'.format(reference)
        token_res = self._get_resp_with_token(referer_url)

        if not token_res:
            return None

        _, token = token_res

        args = {
            '_method': 'PUT',
            '_token': token,
            'proxyUser': username or '',
            'proxyPass': password or '',
            'authIps': '\r\n'.join(authenticated_ips) if authenticated_ips else '',
            'proxyName': proxy_name or ''
        }

        parsed_args = '&'.join(['{}={}'.format(k, quote(v)) for k, v in args.items()])

        res = self._post(
            'https://www.proxies.com/proxy/{}/authSettings'.format(reference),
            body=parsed_args,
            extra_headers={
                # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': len(parsed_args),
                'Referer': referer_url
            }
        )

        return res.status_code == 302

    def get_base_proxy(
        self,
        reference_or_name: str,
    ) -> Optional[BaseProxy]:
        proxies = self.get_proxies(search_term=reference_or_name, show_expired=True)

        return proxies[0] if len(proxies) > 0 else None

    def get_proxy(
        self,
        base_proxy_or_reference_or_name: Union[str, BaseProxy],
    ) -> Optional[Proxy]:
        if type(base_proxy_or_reference_or_name) == str:
            base_proxy = self.get_base_proxy(base_proxy_or_reference_or_name)

            if not base_proxy_or_reference_or_name:
                if self.debug:
                    print('Could not find BaseProxy for reference/name \'{}\''.format(base_proxy_or_reference_or_name))

                return None
        else:
            base_proxy = base_proxy_or_reference_or_name

        additional_proxy_res = self._get(
            'https://www.proxies.com/proxy/{}'.format(base_proxy.reference),
            extra_headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            }
        )

        if not additional_proxy_res:
            if self.debug:
                print('Could not find additional proxy params for reference \'{}\''.format(base_proxy.reference))

            return None

        try:
            return Proxy(base_proxy, additional_proxy_res.content)
        except Exception as e:
            if self.debug:
                print('Could not parse additional proxy params for reference \'{}\''.format(base_proxy.reference))
                print(e)

            return None

    def get_proxies(
        self,
        count: int = 100,
        search_term: Optional[str] = None,
        show_expired: bool = False
    ) -> Optional[List[BaseProxy]]:
        url = 'https://www.proxies.com/proxy/search?draw=2&columns[0][data]=reference&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=name&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=proxy_address&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=server_address&columns[3][name]=&columns[3][searchable]=true&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=server_port&columns[4][name]=&columns[4][searchable]=true&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=country&columns[5][name]=&columns[5][searchable]=true&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=state&columns[6][name]=&columns[6][searchable]=true&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=username&columns[7][name]=&columns[7][searchable]=true&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&columns[8][data]=password&columns[8][name]=&columns[8][searchable]=true&columns[8][orderable]=true&columns[8][search][value]=&columns[8][search][regex]=false&columns[9][data]=created_at&columns[9][name]=&columns[9][searchable]=true&columns[9][orderable]=true&columns[9][search][value]=&columns[9][search][regex]=false&columns[10][data]=updated_at&columns[10][name]=&columns[10][searchable]=true&columns[10][orderable]=true&columns[10][search][value]=&columns[10][search][regex]=false&columns[11][data]=link&columns[11][name]=&columns[11][searchable]=true&columns[11][orderable]=true&columns[11][search][value]=&columns[11][search][regex]=false&order[0][column]=0&order[0][dir]=asc&start=0&length={}&search[value]={}&search[regex]=false&showExpired={}&_={}'.format(count, search_term if search_term else '', 'true' if show_expired else 'false', int(time.time() * 1000))

        try:
            return [BaseProxy(proxy_dict) for proxy_dict in self._get(
                url,
                extra_headers={
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Referer': 'https://www.proxies.com/proxy',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            ).json()['data']]
        except Exception as e:
            if self.debug:
                print('ERROR: get proxies: {}'.format(e))

            return None


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    def _get_resp_with_token(self, url: str) -> Optional[Tuple[Response, str]]:
        try:
            res = self._get(url)
            try:
                token = bs(res.content, 'lxml').find('meta', {'name':'csrf-token'})['content']
            except:
                token = bs(res.content, 'lxml').find('input', {'name':'_token'})['value']

            return res, token
        except Exception as e:
            if self.debug:
                print('ERROR: could not get html data with token for url {}\n{}'.format(url, e))

            return None


# ---------------------------------------------------------------------------------------------------------------------------------------- #