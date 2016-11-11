from concurrent.futures import ThreadPoolExecutor
from tornado import gen
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import curdoc, figure
from bokeh.models.widgets import Slider, Toggle
from bokeh.layouts import row, widgetbox
from bokeh.layouts import gridplot
import numpy as np

# create basic data
doc = curdoc()
executor = ThreadPoolExecutor(max_workers=2)
source = ColumnDataSource(data=dict(x=[0], y=[0], color=["#bad405"]))

# instatiate interactive elements
num_points_slider = Slider(title="offset", value=1, start=1, end=10, step=1)
step_slider = Slider(title="step", value=5, start=1, end=10, step=1)
start_stop = Toggle(label="Start/Stop", button_type="default")

# data management variables
num_points_to_add = 1
step = 0.05
started = False


def update_num_points(attrname, old, new):
    global num_points_to_add
    num_points_to_add = num_points_slider.value


def update_slider(attrname, old, new):
    global step
    step = step_slider.value


def toggle_handler(active):
    global started
    started = active

num_points_slider.on_change('value', update_num_points)
step_slider.on_change('value', update_slider)
start_stop.on_click(toggle_handler)


@gen.coroutine
def update():
    '''update data to be plotted'''
    global started
    global step
    if started:
        new_x = source.data['x'][-1]+step
        new_y = np.sin(new_x)
        source.stream(dict(x=[new_x], y=[new_y], color=["#bad405"]))


# create inputs column
inputs = widgetbox(num_points_slider, step_slider, start_stop, width=100)

# decide tools to be used
tools = "pan,wheel_zoom,box_zoom,reset,save"  # crosshair
hover = HoverTool(tooltips=[("index", "$index"),
                            ("(x,y)", "($x, $y)")])

# prepare figure
p0 = figure(x_range=[0, 10], y_range=[-1, 1], tools=[tools, hover], plot_width=600)
l0 = p0.circle(x='x', y='y', color='color', source=source)

# add plots
p = gridplot([[p0]], toolbar_location='above')

# add plots to document
doc.add_root(row(inputs, p))

doc.add_periodic_callback(update, 100)
