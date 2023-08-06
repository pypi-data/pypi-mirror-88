'''
Yahoo Finance
'''
from pricedb.model import PriceModel, SecuritySymbol
import logging
from decimal import Decimal, InvalidOperation
from datetime import datetime


class YahooWebDownloader:
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

        self.url = 'https://finance.yahoo.com/quote/'

        self.namespaces = {
            'ASX': 'AX'
        }

    def download(self, symbol: SecuritySymbol, currency: str) -> PriceModel:
        import urllib.parse
        import urllib.request

        # if not symbol.namespace:
        #     raise ValueError(f"Namespace not sent for {symbol}")

        # get the translated namespace
        if symbol.namespace in self.namespaces:
            local_namespace = self.namespaces[symbol.namespace]
        else:
            # Take the namespace as is.
            local_namespace = symbol.namespace

        url = self.url + f'{symbol.mnemonic}.{local_namespace}'
        self.logger.debug(f"fetching price from {url}")

        with urllib.request.urlopen(url) as response:
            html = response.read()

        if not html:
            return None

        # parse HTML
        price = self.parse_price(html)
        if price:
            price.symbol = symbol
        # compare currency
        if price.currency != currency:
            raise ValueError(f"Requested currency ({currency}) does not match the {symbol} -> {currency}.")

        return price

    def parse_price(self, html: str) -> PriceModel:
        ''' parse html to get the price '''
        from bs4 import BeautifulSoup
        from pydatum import Datum

        result = PriceModel()
        soup = BeautifulSoup(html, 'html.parser')

        # Price value
        price_el = soup.find(id='last-price-value')
        if not price_el:
            logging.debug(f"Received from mstar: {html}")
            raise ValueError("No price info found in returned HTML.")

        value = price_el.get_text().strip()
        try:
            result.value = Decimal(value)
        except InvalidOperation:
            message = f"Could not parse price value {value}"
            print(message)
            self.logger.error(message)
            return None

        # The rest
        date_str = soup.find(id="asOfDate").get_text().strip()
        date_val = datetime.strptime(date_str, "%m/%d/%Y %H:%M:%S")
        result.datum = Datum()
        result.datum.from_datetime(date_val)

        # tz_str = soup.find(id="timezone").get_text().strip()

        currency = soup.find(id="curency").get_text().strip()
        result.currency = currency

        return result
