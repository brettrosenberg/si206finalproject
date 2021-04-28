import requests as http
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from datetime import datetime, timedelta, timezone
import io

class Crypto:
    def __init__(self, currency='BTC'):
        self.currency = currency
        self.base_url = 'https://api.nomics.com/v1'
        self.API_KEY = 'c49819c7561b7186d23388aa239c7ac0'
        self.data  = None
    
    def retrieve_data(self, days=100):
        if (self.data is None):
            end = datetime.now(timezone.utc).astimezone()
            start = end - timedelta(days = days)
            opts = {
                "currency": self.currency,
                "start": start.isoformat(),
                "end": end.isoformat(),
                "format": "csv",
                "key": self.API_KEY
            }
            r = http.get(self.base_url+'/exchange-rates/history', params=opts).content
            df = pd.read_csv(io.StringIO(r.decode('utf-8')))
            df.columns.values[0] = 'date'
            df.columns.values[1] = 'exchange_rate'
            df['date'] = df['date'].str.split(expand=True)[0]
            df['currency'] = self.currency
            self.data = df
        return self.data

    def plot_crypto_exch_rate(self, df):
        ax = plt.subplot(111)

        colors=[]
        for index, row in df.iterrows():
            if (row['exchange_rate'] >= df['exchange_rate'].mean()):
                colors.append('green')
                continue
            colors.append('red')

        ax.yaxis.set_major_locator(MaxNLocator(10))
        ax.xaxis.set_major_locator(MaxNLocator(10))

        ax.bar(df['date'], df['exchange_rate'], color=colors, width=0.5)
        plt.xlabel("Date")
        plt.ylabel("Exchange Rate $ (USD)")
        plt.xticks(rotation = 45)
        plt.title('{}/USD Exchange Rate'.format(self.currency))
        plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
        plt.show()
    
    def get_name(self):
        return self.currency

if __name__ == '__main__':
    pass