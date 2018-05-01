# Stock Market analysis 
## Installation and Usage 
This Application uses API from alpha_vantage, twitter api, and tensorflow and requires a variety of installations. 
```
pip install alpha_vantage
pip install bokeh
pip install numpy
pip install keras
pip install tensorflow
pip install pandas
```
After installing these packages, find the folder that contains all the files and try using command line to run bokeh server to start the program:
```
bokeh serve --show stock.py
```

Feel free to change the input box content with the company name you like and the date you wish to know about the stock price and twitter data, and then click outside of the input boxes. There is a short latency before you get an updated line chart due to the real-time query.

## 1 StockData interface

### def getSymbolByKeyword(keyword)

This function use API from https://developer.tradier.com

Token are required for this API and it might get expired.

**Exception are raised when keyword matchs no company.**

### def getCompanyNameBySymbol(symbol)

This function relies on the local file: NASDAQ.csv, so place it with the python code file in the same folder.

NASDAQ.csv is a database that contain company's name and stock symbol.

**Exception are raised when keyword matchs no company.**

### def getStockPriceBySymbol(companySymbol, beginDate, endDate)

Using each day's stock close price as Stock price. 

## 2 Twitter interface

The twitter interface uses two functions to get tweets relating the keyword/company name.

### def make_twitter_search(twitter_api, company_name, count, filename) 

Search tweets related to a specific company name.

### def make_twitter_search2(twitter_api, company_name, count, ddl_date, filename)

Search tweets related to a specific company name in a specific day and a limited number of tweets.

## 3 Sentiment Analysis interface

### def convert_text_to_index_array(text)

Parse the input in array of strings to single text.

### def predict_text(text)

Get the result of prediction.

### def postive_rate(texts)

Calculate the overall positive ratio.

Team member:

* Haoran Zhu  696336000

* Jing Tian   631734233

* Shiqi Zhang 778515458

* Yirong Wang 389797398