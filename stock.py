import numpy as np
import pandas as pd 
import urllib3
import certifi
import requests
import sys
import json
import numpy as np
import keras
import keras.preprocessing.text as kpt

from twitter import*
from keras.preprocessing.text import Tokenizer
from keras.models import load_model
from alpha_vantage.timeseries import TimeSeries
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox, layout, column, Spacer
from bokeh.models import ColumnDataSource, Div
from bokeh.models.widgets import Slider, TextInput
from bokeh.models.widgets.inputs import InputWidget
from bokeh.plotting import figure
from os.path import dirname, join

#  =================================================================================
#  Api functions part
#  =================================================================================

#1 ---------------------------- Stock Api: Set up query ----------------------------
def getSymbolByKeyword(keyword):
    url_api = 'https://sandbox.tradier.com/v1/markets/search'
    headers = {'Authorization': 'Bearer iy2BOsFcjIL0AzRA7ZPwpm6A9Qqz',
                'Accept':'application/json'}
    payload = {'q': keyword}
    r = requests.get(url_api, headers=headers, params=payload)
    results = r.json()['securities']
    if results==None:
        raise NameError('No result relate to this keyword, please try another one!')
    else:
        if isinstance(results['security'], dict):
            company_symbol = results['security']['symbol']
        else:
            company_symbol = results['security'][0]['symbol']
        
    return company_symbol

def getCompanyNameBySymbol(symbol):
    companyList = pd.read_csv('NASDAQ.csv')
    symbolToName = companyList.set_index('Symbol')['Name'].to_dict()
    if symbol in symbolToName:
        companyName = symbolToName[symbol]
    else:
        raise NameError('This company is not a NASDAQ-listed company')
    return companyName

def getStockPriceBySymbol(companySymbol, beginDate, endDate):
    ts = TimeSeries(key='1FUQVONDS2O2ARTS', output_format='pandas')
    data= ts.get_daily(symbol=companySymbol, outputsize='full')[0]
    closePrices = data.loc[beginDate:endDate]['4. close'].to_dict()
    return closePrices

keyword = 'facebook'
beginDate = '2018-04-24'
endDate = '2018-04-30'
companySymbol = getSymbolByKeyword(keyword)
companyName = getCompanyNameBySymbol(companySymbol)
stockData = getStockPriceBySymbol(companySymbol, beginDate, endDate)

#1 ---------------------------- End of stock price ------------------------------

#2 ------------------------ Twitter Api: text data ------------------------------
# twitter api authentication step
with open ('test.json', 'r') as f:
    twtr_auth = json.load(f)
CONSUMER_KEY = twtr_auth[0]['consumer_key']
CONSUMER_SECRET = twtr_auth[0]['consumer_secret']
OAUTH_TOKEN = twtr_auth[0]['token']
OAUTH_TOKEN_SECRET = twtr_auth[0]['token_secret']

auth = OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

t = Twitter(auth=auth)

# general twitter search api
def make_twitter_search(twitter_api, company_name, count, filename):
    result = twitter_api.search.tweets(q=company_name,count=count,lang="en")
    with open(filename,'w+')as f:
           for tweet in result["statuses"]:
            print (tweet["created_at"], tweet["user"]["screen_name"], tweet["text"])
            json.dump(tweet,f)
            f.write('\n')

# tweets search by specific date
def make_twitter_search2(twitter_api, company_name, count, ddl_date, filename):
    result = twitter_api.search.tweets(q=company_name,count=count,until=ddl_date,lang="en")
    listResult = []
    for tweet in result["statuses"]:
        listResult.append(tweet["text"])
    return listResult

# test search with date limits
# make_twitter_search2(t,"McDonald's",50,"2018-04-12","search-by-date")

#2 ------------------------------ End of Twitter ------------------------------


#3 --------------------- NLP: get the ratio of text data ----------------------
tokenizer = Tokenizer(num_words=3000)
labels = ['negative', 'positive']

# read in our saved dictionary
with open('saved_models/dictionary.json', 'r') as dictionary_file:
    dictionary = json.load(dictionary_file)

# load the best model we have trained so far
model = load_model('saved_models/best_model.h5')

# makes sure that all the words in your input are registered in the dictionary
def convert_text_to_index_array(text):
    words = kpt.text_to_word_sequence(text)
    wordIndices = []
    for word in words:
        if word in dictionary:
            wordIndices.append(dictionary[word])
    return wordIndices

def predict_text(text):
    # preprocess text
    text_array = convert_text_to_index_array(text)
    preprocessed_text = tokenizer.sequences_to_matrix([text_array], mode='binary')
    
    # predict
    pred = model.predict(preprocessed_text)
    return np.argmax(pred),pred[0][np.argmax(pred)]

def postive_rate(texts):
    postive_num = 0
    negative_num = 0
    for text in texts:
        sentiment, probility = predict_text(text)
        if probility > 0.70:
            if sentiment:
                postive_num += 1
            else:
                negative_num += 1
    total = postive_num + negative_num
    if total:
        return postive_num / total
    else: 
        return 0

#3 -------------------------------- End of NLP --------------------------------------

#  ==================================================================================
#  query data part
#  ==================================================================================

# Set up initial stock price data
df = list(stockData.keys())
x = pd.to_datetime(df)
y = list(stockData.values())
source1 = ColumnDataSource(data=dict(x=x, y=y))

# Set up initial twitter sentiment analysis data
listDate = ['2018-04-24','2018-04-25', '2018-04-26', '2018-04-27', '2018-04-28', '2018-04-29', '2018-04-30']
listValue = []
for date in listDate:
    a = postive_rate(make_twitter_search2(t,"facebook",80000, date, "search-by-date"))
    listValue.append(a)
x1 = pd.to_datetime(listDate)
y1 = listValue
source2 = ColumnDataSource(data=dict(x=x1,y=y1))

#  ==================================================================================
#  Draw graphs and layout
#  ==================================================================================

# Set up stock price plot
plot = figure(plot_height=200, plot_width=600, title="alibaba",
              tools="crosshair,pan,reset,save,wheel_zoom, xbox_select",
              active_drag="xbox_select",
                x_axis_type='datetime')
plot.line(x='x',y= 'y', source=source1, line_width=3, line_alpha=0.6)

# Set up twitter data plot
twitter_plot = figure(plot_height=200, plot_width=600, title="facebook", 
              tools="crosshair,pan,reset,save,wheel_zoom",
                x_axis_type='datetime',)
twitter_plot.line(x='x', y='y', source=source2, color="orange", line_width=3, line_alpha=0.6)

# Set up widgets
text = TextInput(title="company name", value='facebook')
textBegin = TextInput(title="begin date", value='2018-04-24')
textEnd = TextInput(title="end date", value='2018-04-30')
plot.title.text = companyName + ": Stock Price"
twitter_plot.title.text = companyName + ": Public Opinion"
desc = Div(text=open(join(dirname(__file__), "description.html")).read(), width=800)

# Set up callbacks
def update_data(attrname, old, new):
    
    # Get company name and company symbol
    companySymbol = getSymbolByKeyword(text.value)
    companyName = getCompanyNameBySymbol(companySymbol)

    # Update stock data
    plot.title.text = companyName + ": Stock Price"
    stockData = getStockPriceBySymbol(companySymbol, textBegin.value, textEnd.value)
    df = list(stockData.keys())
    x = pd.to_datetime(df)
    y = list(stockData.values())
    source1.data = dict(x=x, y=y)

    # Update twitter data
    twitter_plot.title.text = companyName + ": Public Opinion"
    listValue = []
    for date in listDate:
        a = postive_rate(make_twitter_search2(t,companyName,80000, date, "search-by-date"))
        listValue.append(a)
    x1 = pd.to_datetime(listDate)
    y1 = listValue
    source2.data = dict(x=x1, y=y1)

for w in [text, textBegin, textEnd]:
    w.on_change('value', update_data)

# Set up layouts and add to document
sizing_mode = 'fixed' 

inputs = widgetbox(text, textBegin, textEnd)
space = Spacer(width=300, height=200)
l = layout([
    [desc],
    [inputs, plot],
    [space, twitter_plot],
], sizing_mode=sizing_mode)

curdoc().add_root(l)
curdoc().title = "Stock Prediction"