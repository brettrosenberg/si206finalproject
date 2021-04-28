from api import stock, crypto
from indicators import sma, vwap
from database import db as dbengine
import argparse

ALLOWED_TYPES = ['stock', 'crypto']

store = dbengine.Database()

def write_to_file(df, filename):
    df.to_csv('./{}'.format(filename), index=None, sep='\t')


def print_stock_menu(ticker):
    print('----------------------------------------------')
    print('Action Menu for {}'.format(ticker))
    print('----------------------------------------------')
    print('\t[1] - Retrieve price data and store persistently')
    print('\t[2] - Compute 14 day SMA or VWAP and write to file')
    print('\t[3] - Display chart')
    print('\t[4] - Exit')

def print_crypto_menu(currency):
    print('----------------------------------------------')
    print('Action Menu for {}/USD'.format(currency))
    print('----------------------------------------------')
    print('\t[1] - Retrieve exchange rates and store persistently')
    print('\t[2] - Compute mean and write to file')
    print('\t[3] - Display chart')
    print('\t[4] - Exit')

def handle_stock_cmd(stock, n=0):
    print_stock_menu(stock.get_ticker())
    command = int(input('Enter a command(1-4): '))
    
    if (command == 1):
        data = stock.retrieve_data()
        if (n*25+25 <= data.shape[0]):
            lower = n*25
            upper = lower + 25
            data = data.iloc[lower:upper]
            store.append_stock_df(data)
            print('DONE')

        handle_stock_cmd(stock, n+1)

    elif (command == 2):
        print('------------------------')
        res = store.select_stock_data(stock.get_ticker())
        if res.empty:
            print('No data stored for {}'.format(stock.get_ticker()))

        del res['ticker']
        del res['id']

        indicator = int(input('Enter 1 for SMA-14D, 2 for VWAP: '))

        if (indicator == 1):
            res = sma.compute(res)
            write_to_file(res[['date', 'close', 'SMA_14D']], 'SMA_14D_{}.txt'.format(stock.get_ticker()))
        elif (indicator == 2):
            res = vwap.compute(res)
            write_to_file(res[['date', 'close', 'volume', 'vwap']], 'VWAP_{}.txt'.format(stock.get_ticker()))
        
        handle_stock_cmd(stock)

    elif(command == 3):
        res = store.select_stock_data(stock.get_ticker())
        indicator = int(input('Enter 1 for SMA-14D, 2 for VWAP: '))

        if (indicator == 1):
            res = sma.compute(res)
        elif (indicator == 2):
            res = vwap.compute(res)

        stock.plot_indicator_ohlc(res)
        handle_stock_cmd(stock)

    elif(command == 4):
        print('Thanks for visiting!...')
        print('Exiting program...')
        return

    else:
        print('Command Not Found. Please enter 1-4')
        handle_stock_cmd(stock)

def handle_crypto_cmd(currency, n=0):
    print_crypto_menu(currency.get_name())
    command = int(input('Enter a command(1-4): '))
    
    if (command == 1):
        data = currency.retrieve_data()
        if (n*25+25 <= data.shape[0]):
            lower = n*25
            upper = lower + 25
            data = data.iloc[lower:upper]
            store.append_crypto_df(data)
            print('DONE')
        handle_crypto_cmd(currency, n+1)
    elif (command == 2):
        res = store.select_exchange_rates(currency.get_name())

        mean = sma.compute_crypto(res)
        filename = 'EXCH_RATE_MEAN_{}.txt'.format(currency.get_name())

        write_to_file(res[['date', 'exchange_rate']], filename)
        f = open('./{}'.format(filename), 'a')
        f.write('Average exchange rate over {} days: {}'.format(res.shape[0], mean))
        f.close()

        handle_crypto_cmd(currency)
    elif(command == 3):
        res = store.select_exchange_rates(currency.get_name())
        currency.plot_crypto_exch_rate(res)
        handle_crypto_cmd(currency)
    elif(command == 4):
        print('Thanks for visiting!...')
        print('Exiting program...')
        return

    else:
        print('Command Not Found. Please enter 1-4')
        handle_crypto_cmd(currency)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", help="pull data from stock api or crypto api")
    parser.add_argument("-s", "--symbol", help="asset symbol (ticker or currency pair)")
    args = parser.parse_args()

    if (args is None):
        print("you must specify a -t [stock|crypto]")
        return
    
    if (args.type.lower() in ALLOWED_TYPES):
        if (args.type.lower() == 'stock'):
            s = stock.Stock(args.symbol.upper())
            handle_stock_cmd(s)
        if (args.type.lower() == 'crypto'):
            c = crypto.Crypto(args.symbol.upper())
            handle_crypto_cmd(c)
    else:
        print('you must specify either stock or crypto')
        return

if __name__ == "__main__":
    main()

