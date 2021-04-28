Brett Rosenberg and Maddie Gaudet 
# Report for Final Project SI 206 

## __Goal__

The goal of this project was to allow users to pull stock or crypto data from an API and create simple visualizations with technical indicators using a simple interface.

To achieve this, the project will be using the Alpha Vantage and Nomics API (stocks, and crypto data, respectively). Our project will also use a SQLite3 database as a persistent store.

We wanted to think in terms of tables since we'll be using a SQL database and performing numerical analysis. So we resorted to using the pandas library, which is a great library for handling tabular data. Furthermore, we would require an API to support CSV format in their response bodies. 

## __Features implemented in v1__
* Parse CLI flags to determine whether to load crypto or stock functionality as well as the symbol of the asset itself
* Provides the user 3 distinct options: 1) Retrieve & store, 2) Compute indicators, output to file, and 3) Display Chart 
* Implemented a Simple Moving Average and Volume Weighted Average Price indicator 
* Display a Candlestick chart for Open, High, Low, Close, Volume (OHLCV) stock data
* Insert (0, 25] rows at a time
* Prevent duplicates by keeping `date` column `UNIQUE`Default is `14` days
* Dump pandas dataframe with computed properties onto file `{INDICATOR}-{TICKER}.txt` (i.e VWAP_MSFT.txt)

## __Closed Issues (Problems We Faced)__
> Find an API that returned queries in CSV format, otherwise working with JSON and pandas would be a nightmare. In addition, finding a good, free finance API is *hard*.

**Solution:** The endpoints used from the Alpha Vantage API and Nomics support CSV response formats

> pandas provides a function `to_sql()`, which didn't correctly insert rows or ignore duplicates the way we wanted

**Solution:** Write a manual query that parses the dataframe, extracts the appropriate columns and appends to the database. On any `IntegrityError` we simply swallow the exception silently (the right way to code)

> sqlite3 was storing volume data and returning in byte format, which raised several ValueErrors when calculating indicators, namely VWAP.   

**Solution:** Instead of storing volume in SQL as a `REAL` or `BIGINT` we instead store it as `TEXT`. We then handle parsing from `str` to `float` when data is retrieved from the database. Probably not the nicest way to do it...

> using `pd.read_csv()` and simply passing the response text from the API call was not sufficient and threw many undecipherable errors 

**Solution:** Thanks to the wonderful, beautiful people of Stack Overflow we used: `io.StringIO(response.content.decode('utf-8'))`. For more information: https://stackoverflow.com/questions/32400867/pandas-read-csv-from-url 

> prevent API rate limits (we tested a lot)

**Solution:** Store the API response in a cache, and use that data if it exists

## __Open Issues (Problems We Still Face)__
* No SQL Join: It was difficult to find an appropriate use of a JOIN to perform some computation (for shame!). Perhaps in the future, we could include company info along with OHLCV (but it wouldn't particularly be useful for our purposes). Here's an example query:

```
SELECT * FROM stocks_ohlcv INNER JOIN stock_info ON stocks_ohlcv.ticker = stock_info.ticker WHERE ticker = 'MSFT'; 
```

* No Pagination: The API returns daily time series data for the last 100 days. Our app currently doesn't support handling paginating further than that. 

* Could use better error handling: This app expects the user to behave perfectly and there are some cases like inputing a string instead of an int or a ticker that doesn't exist which cause the app to crash

* Adding new data after the app exits requires multiple calls: Because of the way we've implemented limiting only 25 entries per insert; when Command 1 (Retrieve & Store) is ran, it pulls data from the API and selects the first 25 elements and inserts to the database. Each subsequent call selects the next 25 elements returned from the API (stored in cache). However if the app is exited it will "reset the index" to 0, and since the app ignores duplicates it won't do anything. If the command was run 4 times, meaning 100 items have been added, no new entries will be added. 


## __How to Run__
We've made it really easy for you to test the app without the need to run separate Python scripts!

### Before you Run
Run: `./setup.sh` which will create the virtual environment and install the app's dependencies. Unfortunately there was no extra credit to upload the package to PyPI.

There are two command flags you have to be aware of: `--type` or `-t` and `--symbol` or `-s`. The type specifies either `stock` or `crypto` and the symbol specifies the currency or stock to look up.

### Example Command (Stock)
```
python3 main.py -t stock -s MSFT
```

### Example Command (Crypto)
```
python3 main.py -t crypto -s ETH 
```

After you run that command (feel free to pick any stock or crypto), you will be prompted with 4 options! We recommend you grab some data from the API and store it first :)
It'll look something like:
```
----------------------------------------------
Action Menu for MSFT
----------------------------------------------
	[1] - Retrieve price data and store persistently
	[2] - Compute 14 day SMA or VWAP and write to file
	[3] - Display chart
	[4] - Exit
Enter a command(1-4): 1
```


## Exchange Rates ETH/USD (Mean x&#772;)
| date	     | exchange_rate      |
| ---------- | ---------------    |
| 01/19/2021 | 1368.7006979269888 |
| 01/20/2021 | 1377.9615576169067 |
| 01/21/2021 | 1111.617108871846 |
| 01/22/2021 | 1235.4366962568936 |
| 01/23/2021 | 1234.4899905061552 |
| 01/24/2021 | 1393.4955636711773 |
| 01/25/2021 | 1319.49362245675 |
| 01/26/2021 | 1360.3631970703395 |
| 01/27/2021 | 1243.298797247169 |
| 01/28/2021 | 1330.8647739544701 |
| 01/29/2021 | 1379.7404247839684 |
| 01/30/2021 | 1378.841589279936 |
| 01/31/2021 | 1314.7191255750217 |
| 02/01/2021 | 1375.1155573177386 |
| 02/02/2021 | 1513.655486992227 |
| 02/03/2021 | 1666.680802194203 |
| 02/04/2021 | 1600.0113077821968 |
| 02/05/2021 | 1718.94454518196 |
| 02/06/2021 | 1679.3642899186616 |
| 02/07/2021 | 1615.745377371274 |
| 02/08/2021 | 1752.2035724339005 |
| 02/09/2021 | 1770.6071742840625 |
| 02/10/2021 | 1743.9314677017069 |
| 02/11/2021 | 1787.691304943247 |
| 02/12/2021 | 1845.6240700421708 |
| 02/13/2021 | 1818.6177281785983 |
| 02/14/2021 | 1805.1184902689315 |
| 02/15/2021 | 1780.083284676792 |
| 02/16/2021 | 1784.4877389057158 |
| 02/17/2021 | 1851.9470366265 |
| 02/18/2021 | 1938.702814738286 |
| 02/19/2021 | 1957.3388445502644 |
| 02/20/2021 | 1916.7660181754964 |
| 02/21/2021 | 1936.3271553453844 |
| 02/22/2021 | 1777.786014312352 |
| 02/23/2021 | 1578.8924937360237 |
| 02/24/2021 | 1626.5176988506628 |
| 02/25/2021 | 1483.7251972048412 |
| 02/26/2021 | 1448.950767073747 |
| 02/27/2021 | 1462.6869649769228 |
| 02/28/2021 | 1422.6993255278671 |
| 03/01/2021 | 1573.0103199915363 |
| 03/02/2021 | 1490.4135121645204 |
| 03/03/2021 | 1571.5022835202844 |
| 03/04/2021 | 1542.1784345726146 |
| 03/05/2021 | 1531.6240063346054 |
| 03/06/2021 | 1651.9007669622797 |
| 03/07/2021 | 1726.732047322852 |
| 03/08/2021 | 1834.9597147593367 |
| 03/09/2021 | 1869.1948164702123 |
**Average exchange rate over 50 days**: 1590.015231532552

## Crypto Visualization
![Crypto Example](/images/crypto-example.png)

Displays a bar chart with a color mask if the exchange rate traded below the average of X stored data points (red) or above the mean (green)


## Volume Weighted Average Price (VWAP) for Microsoft (MSFT)
| date	     | close  | volume     | vwap	            |
| ---------- | ------ | ---------- | ------------------ |
| 2021-04-26 | 261.55 | 19763346.0 | 261.3025           | 
| 2021-04-23 | 261.15 | 21499286.0 | 260.3060200741678 |
| 2021-04-22 | 257.17 | 25606152.0 | 259.6948539938307 |
| 2021-04-21 | 260.58 | 24030383.0 | 259.50190755015393 |
| 2021-04-20 | 258.26 | 19722875.0 | 259.326842621654   |
| 2021-04-19 | 258.74 | 23209260.0 | 259.3829718539987 |
| 2021-04-16 | 260.74 | 24878582.0 | 259.37007532219855 |
| 2021-04-15 | 259.5  | 25627481.0 | 259.29499141255167 |
| 2021-04-14 | 255.59 | 23070938.0 | 259.0391532493152 |
| 2021-04-13 | 258.49 | 23837469.0 | 258.93306521810655 |
| 2021-04-12 | 255.91 | 27148668.0 | 258.64013222400376 |
| 2021-04-09 | 255.85 | 24326833.0 | 258.2593704529705 |
| 2021-04-08 | 253.25 | 23625197.0 | 257.8591317563865 |
| 2021-04-07 | 249.9  | 22719835.0 | 257.2516103583863 |
| 2021-04-06 | 247.86 | 22931923.0 | 256.6580086566626 |
| 2021-04-05 | 249.07 | 36910609.0 | 255.67779670721112 |
| 2021-04-01 | 242.35 | 30337982.0 | 254.57550856936376 |
| 2021-03-31 | 235.77 | 43623471.0 | 252.80081669080124 |
| 2021-03-30 | 231.85 | 24792012.0 | 251.76748298991544 |
| 2021-03-29 | 235.24 | 25227455.0 | 250.91027920120465 |
| 2021-03-26 | 236.48 | 25479853.0 | 250.11610538566245 |
| 2021-03-25 | 232.34 | 34061853.0 | 249.17230918474692 |
| 2021-03-24 | 235.46 | 25620127.0 | 248.6362902931719 |
| 2021-03-23 | 237.58 | 31638376.0 | 248.15513561493376 |
| 2021-03-22 | 235.99 | 30127005.0 | 247.48690059942854 |
| 2021-03-19 | 230.35 | 46430730.0 | 246.39720640351797 |
| 2021-03-18 | 230.72 | 34852251.0 | 245.7323656290927 |
| 2021-03-17 | 237.04 | 29562100.0 | 245.35481882215092 |
| 2021-03-16 | 237.71 | 28092196.0 | 245.09606183537576 |
| 2021-03-15 | 234.81 | 26042669.0 | 244.72984137488547 |
| 2021-03-12 | 235.75 | 22653662.0 | 244.45705021396245 |
| 2021-03-11 | 237.13 | 29907586.0 | 244.19398963944738 |
| 2021-03-10 | 232.42 | 29746812.0 | 243.87674923355047 |
| 2021-03-09 | 233.78 | 33080531.0 | 243.51259040374936 |
| 2021-03-08 | 227.39 | 35267440.0 | 243.03299189428972 |
| 2021-03-05 | 231.6  | 41872770.0 | 242.49100196304582 |
| 2021-03-04 | 226.73 | 44727785.0 | 241.89651449223646 |
| 2021-03-03 | 227.56 | 34029526.0 | 241.54020749774213 |
| 2021-03-02 | 233.87 | 22812459.0 | 241.4145089452168 |
| 2021-03-01 | 236.94 | 25332837.0 | 241.27935713443264 |
| 2021-02-26 | 232.38 | 37545055.0 | 240.99900645167153 |
| 2021-02-25 | 228.99 | 39118089.0 | 240.68608497872557 |
| 2021-02-24 | 234.55 | 26339746.0 | 240.50475909884526 |
| 2021-02-23 | 233.27 | 30228704.0 | 240.29830396366046 |
| 2021-02-22 | 234.51 | 36182764.0 | 240.1569130601362 |
| 2021-02-19 | 240.97 | 25262600.0 | 240.19206597253756 |
| 2021-02-18 | 243.79 | 16925563.0 | 240.21956637848913 |
| 2021-02-17 | 244.2  | 21451617.0 | 240.25703178021593 |
| 2021-02-16 | 243.7  | 26728487.0 | 240.3382820960193 |
| 2021-02-12 | 244.99 | 16561079.0 | 240.3811454034937 |
| 2021-02-11 | 244.49 | 15751059.0 | 240.41699243682632 |
| 2021-02-10 | 242.82 | 22117240.0 | 240.46230555600425 |
| 2021-02-09 | 243.77 | 23471475.0 | 240.50360790262567 |
| 2021-02-08 | 242.47 | 22211929.0 | 240.52932365778938 |
| 2021-02-05 | 242.2  | 18054752.0 | 240.54498836733657 |
| 2021-02-04 | 242.01 | 25296100.0 | 240.56558457989192 |
| 2021-02-03 | 243.0  | 27158104.0 | 240.59334259081828 |
| 2021-02-02 | 239.51 | 25678356.0 | 240.59184482931374 |
| 2021-02-01 | 239.65 | 33314193.0 | 240.52807970756763 |
| 2021-01-29 | 231.96 | 42503138.0 | 240.37991132926206 |
| 2021-01-28 | 238.93 | 49111159.0 | 240.33678743272705 |
| 2021-01-27 | 232.9  | 69870638.0 | 240.14035254907745 |
| 2021-01-26 | 232.33 | 49169601.0 | 239.9267917626536 |
| 2021-01-25 | 229.53 | 33152095.0 | 239.69852769839372 |
| 2021-01-22 | 225.95 | 30172663.0 | 239.5124634743018 |
| 2021-01-21 | 224.97 | 30749553.0 | 239.27208867254106 |
| 2021-01-20 | 224.34 | 37777260.0 | 238.93311595432806 |
| 2021-01-19 | 216.44 | 30480859.0 | 238.56660482714562 |
| 2021-01-15 | 212.65 | 31746512.0 | 238.17262168630074 |
| 2021-01-14 | 213.02 | 29346737.0 | 237.84515427072984 |
| 2021-01-13 | 216.34 | 20087080.0 | 237.62865931734885 |
| 2021-01-12 | 214.93 | 23148341.0 | 237.3828199087494 |
| 2021-01-11 | 217.49 | 23047029.0 | 237.17154182355682 |
| 2021-01-08 | 219.62 | 22956206.0 | 236.97604724368017 |
| 2021-01-07 | 218.29 | 27694480.0 | 236.71679103444708 |


## Stock Visualization (VWAP)
![Stock Example](/images/stock-example.png)

Displays a Candlestick OHLC(Open, High, Low, Close) Chart for a given ticker, with the VWAP indicator overlayed

## __Docs__
Project Structure

```
api/
   | crypto.py
   | stock.py
database/
   | db.py
   | query.py
indicators/
   | sma.py
   | vwap.py
main.py
```

We tried to keep things consistent, so you'll find that most functions simply require a pandas DataFrame to be passed.


### Main

`write_to_file(df, filename)`
Method: Write the contents of a dataframe to a file  
Params: 
> df: `pd.Dataframe` - the dataframe to output to file

> filename: `str` - the name of the file (not full path)

Returns: `None`  

`print_stock_menu(ticker)`  
Method: Print the stock action menu to the console  
Params: 
> ticker: `str` - the ticker to display  

Returns: `None`  

`print_crypto_menu(currency)`  
Method: Print the crypto action menu to the console  
Params: 
> currency: `str` - the currency to display  

Returns: `None`  

`handle_stock_cmd(stock,n=0)`  
Method: Handles mapping each user input to the appropriate `Stock` function as well as displays the action menu  
Params:  
> stock: `stock.Stock` - the `Stock` class that you'll be manipulating.Created in `main()` after parsing flags 

> n: `int` Default: 0 - keeps track of how many times a command was run, only used for handling appending data to the database

Returns: `None`   

`handle_crypto_cmd(crypto,n=0)`  
Method: Handles mapping each user input to the appropriate `Crypto` function as well as displays the action menu  
Params:  
> crypto: `crypto.Crypto` - the `Crypto` class that you'll be manipulating. Created in `main()` after parsing flags  

> n: `int` Default: 0 - keeps track of how many times a command was run, only used for handling appending data to the database

Returns: `None`   

### Crypto
When a Crypto class is initialized, you pass a `currency` parameter to the constructor, which is the currency we will be querying from the API. It'll set some constants like `API_KEY` and `base_url` used in the following functions:


`Crypto.retrieve_data(days)`  
Method: Retrieves data from the API and parses into a dataframe. If data is cached (`self.data` exists), returns cached. In this case the endpoint is:`https://api.nomics.com/v1/exchange-rates/history`  
Params: `None`   
Returns: `pd.DataFrame`  

`Crypto.plot_crypto_exch_rate(df)`  
Method: Takes a pandas dataframe and renders a bar chart with a color mask. If the exchange rate trades below the average of the dataset, it will be displayed in red, otherwise green. Displays only 10 ticks on both y and x axis. 
Params:  
> df: `pd.DataFrame` - the dataframe to render

Returns: `None`

### Stock
When a Stock class is initialized, you pass a `ticker` parameter to the constructor, which is the stock to be queried from Alpha Vantage. It'll set some constants like `ALPHA_VANTAGE_KEY` and `base_url` used in the following functions:


`Stock.retrieve_data(days)`  
Method: Retrieves data from the API and parses into a dataframe. If data is cached (`self.data` exists), returns cached. In this case the endpoint is: `https://www.alphavantage.co/query` 
Params: `None`  
Returns: `pd.DataFrame`  

`Stock.plot_indicator_ohlc(df)`  
Method: Takes a pandas dataframe and renders a Candlestick chart. When an indicator is computed on a dataframe, it will append a column to the dataframe. Depending on what indicator is present, it will render the correct indicator. As of now only one indicator at a time is supported, with VWAP and 14-Day SMA being the two available.  
Params:   
> df: `pd.DataFrame` - the dataframe to render

Returns: `None`

### Database
When the DB class is initialized it looks for a file called `store.db` in the root of the project's directory; if it doesn't exist, `sqlite3` will take care of creating it. 


`Database.append_stock_df(df)`  
Method: Takes a pandas dataframe and loops through each row, running an `INSERT` statement in `stocks_ohlcv` table. It will safely handle any `IntegrityError` (meaning a duplicate row). The function also handles converting volume to `str`  
Params:  
> df: `pd.DataFrame` - the dataframe to append to the database

Returns: `None`

`Database.append_crypto_df(df)`  
Method: Takes a pandas dataframe and loops through each row, running an `INSERT` statement in `exchange_rates` table. It will safely handle any `IntegrityError` (meaning a duplicate row)  
Params:  
> df: `pd.DataFrame` - the dataframe to append to the database

Returns: `None`

`Database.select_stock_data(ticker)`  
Method: Takes a ticker and performs a `SELECT` query where the ticker column matches the ticker parameter. The function handles converting volume from `str` to `float` 
Params:
> ticker: `str` - the ticker to query the database for

Returns: `pd.DataFrame`

`Database.select_exchange_rates(currency)`  
Method: Takes a currency and performs a `SELECT` query where the currency column matches the currency parameter. 
Params:
> ticker: `str` - the ticker to query the database for

Returns: `pd.DataFrame`

### SMA
`sma.compute(df, days=14)`
Method: Computes a simple moving average for X number of days on `df` using `close` price data and appends a column to `df`. Default is `14` days  
Params:  
> df: `pd.DataFrame` 

> days: `int` Default: `14`

Returns: `pd.DataFrame`

### VWAP 
`vwap.compute(df, days=14)`
Method: Computes the volume weighted average price on `df` using `close` price and `volume` data and appends a column to `df`.  
Params:  
> df: `pd.DataFrame` 

Returns: `pd.DataFrame`

### Resources Used
| Date | Issue Description | Resource URL | Result |
| ---- | ----------------- | ------------ | ------ |
| 4/15 | Find a good finance API (stock) | https://medium.com/@patrick.collins_58673/stock-api-landscape-5c6e054ee631 | Found Alpha Vantage |
| 4/15 | Find a good finance API (crypto) | https://medium.com/coinmonks/best-crypto-apis-for-developers-5efe3a597a9f | Found Nomics |
| 4/15 | Learn pandas |  https://www.youtube.com/watch?v=nLw1RNvfElg&list=PLQVvvaa0QuDfSfqQuee6K8opKtZsh7sA9 | Well, kinda |
| 4/17 | using `pd.read_csv()` and simply passing the response text from the API call was not sufficient and threw many undecipherable error |  https://stackoverflow.com/questions/32400867/pandas-read-csv-from-url | Parse csv response text correctly |
| 4/21 | sqlite3 was storing volume data and returning in byte format, which raised several ValueErrors when calculating indicators, namely VWAP | SQLite3 Docs + Debugging/Trial and Error | A rather ugly hackaround, but got volume data to be the right type. |
| 4/25 | create an OHLC candlestick chart, matplotlib's API is horrendous | https://pypi.org/project/finplot/ | Turns out finplot's API is not *great*, but at least easy to create a viewable candlestick chart. Unable to figure out how to add axis labels. | 


