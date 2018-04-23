import numpy as np
import pandas as pd 

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure


# Set up data
N = 200

stockData = {'2018-03-01': 92.849999999999994, '2018-03-02': 93.049999999999997, '2018-03-05': 93.640000000000001, '2018-03-06': 93.319999999999993, '2018-03-07': 93.859999999999999, '2018-03-08': 94.430000000000007, '2018-03-09': 96.540000000000006}
#data = {'2018-03-01': 1, '2018-03-02': 2}
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

    # Get the current slider values


    # Generate the new curve
    x = np.linspace(0, 4*np.pi, N)


    source.data = dict(x=x, y=y)




# Set up layouts and add to document
inputs = widgetbox(text, textBegin, textEnd)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"