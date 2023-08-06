# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from datetime import datetime

# Pip
from jsoncodable import JSONCodable

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ----------------------------------------------------------- class: BaseProxy ----------------------------------------------------------- #

class BaseProxy:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        d: dict
    ):
        self.reference = d['reference']
        self.web_url = 'https://www.proxies.com/proxy/{}'.format(d['reference'])

        self.proxy_address = d['proxy_address']
        self.server_address = d['server_address']
        self.server_port = int(d['server_port'])

        self.username = d['username'] if d['username'] else None
        self.password = d['password'] if d['password'] else None

        self.created_at = d['created_at']
        self.updated_at = d['updated_at']

        self.date_created_at = datetime.strptime(self.created_at, '%Y-%m-%d %H:%M:%S')
        self.date_updated_at = datetime.strptime(self.updated_at, '%Y-%m-%d %H:%M:%S')

        self.ts_created_at = int(self.date_created_at.timestamp())
        self.ts_updated_at = int(self.date_updated_at.timestamp())

        self.name = d['name'] if d['name'] else None
        self.country = d['country']
        self.state = d['state']

        self.url = '{}:{}'.format(self.server_address, self.server_port)

        if self.username and self.password:
            self.url = '{}:{}@{}'.format(self.username, self.password, self.url)

        self.url_ftp = 'ftp://{}'.format(self.url)
        self.url_http = 'http://{}'.format(self.url)
        self.url_https = 'https://{}'.format(self.url)


# ---------------------------------------------------------------------------------------------------------------------------------------- #