# Stock Market analysis 

## This program can obtain StockData by keyword.

### def getSymbolByKeyword(keyword)

This function use API from https://developer.tradier.com

Token are required for this API and it might get expired.

**Exception are raised when keyword matchs no company.**

### def getCompanyNameBySymbol(symbol)

This function rely on the local file: NASDAQ.csv, so place it with the python code file in the same folder.

NASDAQ.csv is a database that contain company's name and stock symbol.

**Exception are raised when keyword matchs no company.**

### def getStockPriceBySymbol(companySymbol, beginDate, endDate)

This function use API from alpha_vantage and require installation. *pip install alpha_vantage*

Using each day's stock close price as Stock price. 