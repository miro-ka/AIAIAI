import logging
import requests
import pandas as pd
from urllib.parse import urlencode


ROOT_URL = "https://poloniex.com/public?"
FETCH_INTERVAL = 24*3600 # 1day


class Poloniex:
    def __init__(self):
        self.root_url = ROOT_URL
        self.log = logging.getLogger(self.__class__.__name__)

    def get_pairs(self):
        """
        Get list of all tickers
        :return: List of all available tickers
        """
        self.log.info("Starting to fetch all available pairs..")
        url = self.root_url + "command=returnTicker"
        response = requests.request("GET", url)
        if response.status_code != 200:
            self.log.error("Got non 200 response. Quitting..")
            exit()

        pairs = []
        for key, value in response.json().items():
            if value['isFrozen'] == '0':
                pairs.append(key)
            else:
                self.log.info("Pair " + key + " is frozen and will be skipped.")

        self.log.info("Got total pairs " + str(len(pairs)))
        return pairs

    def fetch(self,
              fetch_from,
              fetch_to,
              path,
              ticker,
              pairs):
        """
        Fetch Ticker data and store them in path (local or gcp storage)
        :param fetch_from: UTC time fetch data from
        :param fetch_to: UTC time fetch data to
        :param path: local og gs:// (cloud storage)
        :param ticker: 300, 900, 1800, 7200, 14400, and 86400
        :param pairs: List of pairs to be fetched ('all' for all)
        :return:
        """

        if pairs == 'all':
            pairs = self.get_pairs()

        # TO BE REMOVED!
        pairs = ['BTC_XMR']
        df = pd.DataFrame()
        for pair in pairs:
            fetch_from_tmp = fetch_from
            while fetch_from_tmp < fetch_to:
                encode_payload = {
                    'command': 'returnChartData',
                    'currencyPair': pair,
                    'start': fetch_from_tmp,
                    'end': fetch_from_tmp + FETCH_INTERVAL,
                    'period': ticker
                }
                self.log.info("Fetching ticker data for " + pair + ": " + str(encode_payload['start']) + '-' + str(encode_payload['end']))
                query_string = urlencode(encode_payload)
                url = self.root_url + query_string
                response = requests.request("GET", url)
                if response.status_code != 200:
                    self.log.error("Didn't get 200. Details: " + str(response.status_code))
                fetch_from_tmp += FETCH_INTERVAL

                # If we got empty ticker, just continue
                if response.text == '':
                    self.log.warning("Got empty ticker for " + pair)
                    continue
                ticker_data = response.json()
                df_ticker = pd.DataFrame(response.json())
                df_ticker['pair'] = pair
                df = df.append(df_ticker)
                with open('workir/backfill.csv', 'a') as f:
                    df.to_csv(f, header=f.tell() == 0, index=False)

        return True
