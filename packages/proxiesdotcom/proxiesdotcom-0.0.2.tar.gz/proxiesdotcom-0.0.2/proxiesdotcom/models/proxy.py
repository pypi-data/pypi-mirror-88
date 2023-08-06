# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from datetime import datetime

# Pip
from jsoncodable import JSONCodable
from bs4 import BeautifulSoup as bs

# Local
from .base_proxy import BaseProxy

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------- class: Proxy ------------------------------------------------------------- #

class Proxy(JSONCodable):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        base_proxy: BaseProxy,
        html_str_or_content
    ):
        for attr, value in base_proxy.__dict__.items():
            setattr(self, attr, value)

        soup = bs(html_str_or_content, 'lxml')
        lis = soup.find_all('li', class_='list-group-item')

        self.paid_until = lis[3].find('p').text.strip()
        self.date_paid_until = datetime.strptime(self.paid_until, '%Y-%m-%d %H:%M:%S')
        self.ts_paid_until = int(self.date_paid_until.timestamp())

        self.domains = [li.text.strip() for li in lis[4].find_all('li')]

        self.authenticated_ips = [li.text.strip() for li in lis[6].find_all('li')]


# ---------------------------------------------------------------------------------------------------------------------------------------- #