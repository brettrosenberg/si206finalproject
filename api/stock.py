import requests as http 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import finplot as fplt
import io
import datetime as dt
from mplfinance.original_flavor import candlestick2_ohlc
import matplotlib.dates as mdates


class Stock:
    def __init__(self, ticker="AAPL"):
        self.ticker = ticker
        self.base_url = 'https://www.alphavantage.co/query'
        self.ALPHA_VANTAGE_KEY = "QDPV653ZW8TI02T5"
        self.data = None 

    def retrieve_data(self):
        if (self.data is None):
            opts = {
                "function": "TIME_SERIES_DAILY",
                "symbol": self.ticker,
                "outputsize": "compact",
                "datatype": "csv",
                "apikey": self.ALPHA_VANTAGE_KEY
            }
            r = http.get(self.base_url, params=opts).content
            df = pd.read_csv(io.StringIO(r.decode('utf-8')))
            df = df.rename(columns={'timestamp': 'date'})
            df = df.rename(columns={'index': 'id'})
            df['ticker'] = self.ticker
            self.data = df
        return self.data

    def plot_indicator_ohlc(self, df):
        df['date'] = pd.to_datetime(df['date'])
        ax = fplt.create_plot('{} Price Data (Last 100 Days)'.format(self.ticker), rows=1)
        candles = df[['date', 'open', 'close', 'high', 'low']]
        fplt.candlestick_ochl(candles, ax=ax)
        if ('SMA_14D' in df.columns):
            fplt.plot(df['SMA_14D'], legend='14-Day SMA')
        else:
            fplt.plot(df['vwap'], legend='VWAP')
        fplt.autoviewrestore()
        fplt.show()

    def get_ticker(self):
        return self.ticker

if __name__ == '__main__':
    pass