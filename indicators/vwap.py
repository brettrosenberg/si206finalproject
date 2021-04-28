import pandas as pd
def compute(data):
    data['vwap'] = (data['volume']*(data['high']+data['low'])/2).cumsum() / data['volume'].cumsum()
    return data