import pandas as pd
import numpy as np
def compute(df, days=14):
    col_name = 'SMA_{}D'.format(days)
    for i in range(0, df.shape[0]-days):
        sum = 0
        for j in range(0, days):
            sum = sum + df.iloc[i+j,1]
        df.loc[df.index[i+2], col_name] = np.round(sum / days, 1)
    return df

def compute_crypto(df):
    return df['exchange_rate'].mean()

if __name__ == '__main__':
    pass