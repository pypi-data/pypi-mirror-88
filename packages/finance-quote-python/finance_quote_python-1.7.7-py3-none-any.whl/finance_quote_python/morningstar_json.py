'''
Morningstar API
This should replace the standard Morningstar module.

Requires authentication!
'''
import logging
from pricedb.model import PriceModel, SecuritySymbol

class MorningstarApiDownloader:
    ''' Uses Morningstar JSON API '''
    def __init__(self):
        super().__init__()
        self.url = 'https://api-global.morningstar.com/sal-service/v1/etf/quote/v1/F00000O2BY/data?'
        self.params = { 't': 'symbol' }

        self.logger = logging.getLogger(__name__)

    def download(self, symbol: SecuritySymbol, currency: str) -> PriceModel:
        pass