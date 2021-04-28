import pandas as pd
import numpy as np
def compute(df, days=14):
    df['SMA_14D'] = df['close'].rolling(days).mean()
    return df

def compute_crypto(df):
    return df['exchange_rate'].mean()

if __name__ == '__main__':
    pass