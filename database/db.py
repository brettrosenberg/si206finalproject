import sqlite3
import pandas as pd
from .query import create_stock_ohlc_table, create_exchange_rate_table, insert_stock_row, insert_crypto_row 
import sys
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('./store.db') 
        self.cursor = self.conn.cursor()
        self.cursor.execute(create_stock_ohlc_table())
        self.cursor.execute(create_exchange_rate_table())
        self.conn.commit()

    def append_stock_df(self, df):
        for i in range(len(df)):
            try:
                row = df.iloc[i:i+1]
                self.cursor.execute(
                    insert_stock_row(),
                    ( 
                        row['date'].values[0],
                        row['open'].values[0],
                        row['high'].values[0],
                        row['low'].values[0],
                        row['close'].values[0],
                        str(row['volume'].values[0]),
                        row['ticker'].values[0]
                    ),
                )
                self.conn.commit()
            except:
                pass

    
    def append_crypto_df(self, df):
        for i in range(len(df)):
            try:
                row = df.iloc[i:i+1]
                self.cursor.execute(
                    insert_crypto_row(),
                    (
                        row['date'].values[0],
                        row['exchange_rate'].values[0],
                        row['currency'].values[0],
                    )
                )
                self.conn.commit()
            except:
                e = sys.exc_info()[0]
                pass
        # return df.to_sql('exchange_rates', con=self.conn, if_exists='append')

    def select_stock_data(self, ticker):
        df = pd.read_sql_query("SELECT * FROM stock_ohlcv WHERE ticker = '{}'".format(ticker), self.conn)
        df['volume'] = df['volume'].astype(float)
        return df
    
    def select_exchange_rates(self, currency):
        return pd.read_sql_query("SELECT * FROM exchange_rates WHERE currency = '{}'".format(currency), self.conn)
    
    def close_connection(self):
        self.cursor.close()
    
if __name__ == '__main__':
    pass
