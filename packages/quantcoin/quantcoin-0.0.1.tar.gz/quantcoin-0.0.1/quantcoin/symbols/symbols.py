import requests
import logging
import pandas as pd


class Symbols(object):
    def __init__(self):
        """

        """
        self.baseurl = "https://data.quantcoin.co/data/"
        self.logger = logging.getLogger(__name__)

    def __getattr__(self, symb):
        self.logger.debug("__getattr__ called with item:".format(symb))
        url = "{}{}.csv.gz".format(self.baseurl, symb)
        self.logger.debug("getting symb data from {}".format(url))
        self[symb] = pd.read_csv(url, compression="gzip", parse_dates=True, infer_datetime_format=True)
        return self[symb]