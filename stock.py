import numpy as np
import pandas as pd 
import urllib3
import certifi
import requests
import sys

from alpha_vantage.timeseries import TimeSeries
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure

# Set up query
def getSymbolByKeyword(keyword):
    url_api = 'https://sandbox.tradier.com/v1/markets/search'
    headers = {'Authorization': 'Bearer iy2BOsFcjIL0AzRA7ZPwpm6A9Qqz',
                'Accept':'application/json'}
    payload = {'q': keyword}
    r = requests.get(url_api, headers=headers, params=payload)
    # print(r.url)
    results = r.json()['securities']
    # print(results)
    if results==None:
        #print('No result relate to this keyword, please try another one!')
        raise NameError('No result relate to this keyword, please try another one!')
    else:
        if isinstance(results['security'], dict):
            company_symbol = results['security']['symbol']
        else:
            company_symbol = results['security'][0]['symbol']
        
    return company_symbol

def getCompanyNameBySymbol(symbol):
    companyList = pd.read_csv(filepath_or_buffer=sys.path[0]+'\\NASDAQ.csv')
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

keyword = 'microsoft'
beginDate = '2018-03-01'
endDate = '2018-03-10'
companySymbol = getSymbolByKeyword(keyword)
companyName = getCompanyNameBySymbol(companySymbol)
stockData = getStockPriceBySymbol(companySymbol, beginDate, endDate)

# Set up data

df = list(stockData.keys())
x = pd.to_datetime(df)
y = list(stockData.values())
source = ColumnDataSource(data=dict(x=x, y=y))


# Set up plot
plot = figure(plot_height=400, plot_width=400, title="microsoft",
              tools="crosshair,pan,reset,save,wheel_zoom",
                x_axis_type='datetime')
                #x_range=['2018-03-01','2018-03-10'], y_range=[80, 100])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)


# Set up widgets
text = TextInput(title="company name", value='microsoft')
textBegin = TextInput(title="begin date", value='2018-03-01')
textEnd = TextInput(title="end date", value='2018-03-10')


# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)

def update_data(attrname, old, new):
    # TODO: implement the onchange update
    # Get the current slider values


    # Generate the new curve


    source.data = dict(x=x, y=y)




# Set up layouts and add to document
inputs = widgetbox(text, textBegin, textEnd)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"