import logging
from exchange.poloniex.poloniex import Poloniex
from exchange.exchanges import Exchanges


class Fetch:
    """
    Simple class for fetching ticker data
    """
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)

    def fetch(self,
              fetch_from,
              fetch_to,
              path,
              ticker,
              pairs,
              exchange=Exchanges.Poloniex):
        """
        Fetch Ticker data and store them in path (local or gcp storage)
        :param fetch_from: UTC time fetch data from
        :param fetch_to: UTC time fetch data to
        :param path: local og gs:// (cloud storage)
        :param ticker: 300, 900, 1800, 7200, 14400, and 86400
        :param pairs: List of pairs to be fetched ('all' for all)
        :param exchange: Exchange from where data should be fetched
        :return:
        """

        if exchange == Exchanges.Poloniex:
            return Poloniex().fetch(
                fetch_to=fetch_to,
                fetch_from=fetch_from,
                path=path,
                ticker=ticker,
                pairs=pairs)
        else:
            self.log.warn("Invalid or not supported exchange!")
            return False
