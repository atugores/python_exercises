from concurrent.futures import ThreadPoolExecutor

from bokeh.models import ColumnDataSource
from bokeh.plotting import curdoc, figure
from bokeh.models.widgets import Slider, Toggle
from bokeh.layouts import row, widgetbox
from bokeh.layouts import gridplot

# create basic data
doc = curdoc()
executor = ThreadPoolExecutor(max_workers=2)
source = ColumnDataSource(data=dict(x=[0], y=[0], color=["blue"]))

# instatiate interactive elements
num_points_slider = Slider(title="offset", value=1, start=1, end=10, step=1)
step_slider = Slider(title="step", value=5, start=1, end=10, step=1)
start_stop = Toggle(label="Start/Stop", button_type="default")

# create inputs column
inputs = widgetbox(num_points_slider, step_slider, start_stop, width=100)

# prepare figure
p0 = figure(x_range=[0, 100], y_range=[0, 20], plot_width=600)
l0 = p0.circle(x='x', y='y', color='color', source=source)

# add plots
p = gridplot([[p0]])

# add plots to document
doc.add_root(row(inputs, p))
