
def create_stock_ohlc_table():
    return '''
    CREATE TABLE IF NOT EXISTS stock_ohlcv (
        "id" BIGSERIAL PRIMARY KEY,
        "date" TEXT UNIQUE,
        "open" REAL,
        "high" REAL,
        "low" REAL,
        "close" REAL,
        "volume" TEXT,
        "ticker" TEXT
    );
    '''

def create_exchange_rate_table():
    return '''
    CREATE TABLE IF NOT EXISTS exchange_rates (
        "id" BIGSERIAL PRIMARY KEY,
        "date" TEXT UNIQUE,
        "exchange_rate" REAL,
        "currency" TEXT
    )
    '''
def insert_stock_row():
    return '''
    INSERT INTO stock_ohlcv (date, open, high, low, close, volume, ticker)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    '''

def insert_crypto_row():
    return '''
    INSERT INTO exchange_rates (date, exchange_rate, currency)
    VALUES (?, ?, ?)
    '''

def create_index(table, index):
    return 'CREATE INDEX on {} ({});'.format(table, index)