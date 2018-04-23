''' Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve sliders.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/sliders
in your browser.
'''
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure

import urllib3
import certifi
import requests
import pandas as pd
import sys
from alpha_vantage.timeseries import TimeSeries

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
    #closePrices = data.loc[beginDate:endDate]['4. close'].to_dict()
    return data

keyword = 'microsoft'
beginDate = '2018-03-01'
endDate = '2018-03-10'
companySymbol = getSymbolByKeyword(keyword)
companyName = getCompanyNameBySymbol(companySymbol)
#stockData = getStockPriceBySymbol(companySymbol, beginDate, endDate)
stockData = {'2018-03-01': 92.849999999999994, '2018-03-02': 93.049999999999997, '2018-03-05': 93.640000000000001, '2018-03-06': 93.319999999999993, '2018-03-07': 93.859999999999999, '2018-03-08': 94.430000000000007, '2018-03-09': 96.540000000000006}

# Set up data
#N = 200
x = stockData.keys()
y = stockData.values()
source = ColumnDataSource(data=dict(x=x, y=y))
#source = ColumnDataSource(data=stockData)



# Set up plot
plot = figure(plot_height=400, plot_width=400, title="my sine wave",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, 4*np.pi], y_range=[-2.5, 2.5])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)


# Set up widgets
text = TextInput(title="company name", value='microsoft')
text1 = TextInput(title="begin time", value=beginDate)
text2 = TextInput(title="end time", value=endDate)



# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)

def update_data(attrname, old, new):

    # Get the current slider values
    #a = amplitude.value
    #b = offset.value
    #w = phase.value
    #k = freq.value

    # Generate the new curve
    #x = np.linspace(0, 4*np.pi, 200)
    #y = a*np.sin(k*x + w) + b

    source.data = source

#for w in [offset, amplitude, phase, freq]:
#    w.on_change('value', update_data)


# Set up layouts and add to document
inputs = widgetbox(text, text1, text2)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"