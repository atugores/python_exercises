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
source_sin = ColumnDataSource(data=dict(x=[0], y=[0], color=["#bad405"]))
source_cos = ColumnDataSource(data=dict(x=[0], y=[1], color=["#666666"]))

# instatiate interactive elements
yoffset_slider = Slider(title="offset", value=0, start=-10, end=10, step=1)
step_slider = Slider(title="step (*0.001)", value=5, start=1, end=100, step=10)
start_stop = Toggle(label="Start/Stop", button_type="default")

# data management variables
yoffset = 0
step = 0.05
started = False


def update_yoffset(attrname, old, new):
    global yoffset
    yoffset = yoffset_slider.value


def update_slider(attrname, old, new):
    global step
    step = step_slider.value / 100.0


def toggle_handler(active):
    global started
    started = active

yoffset_slider.on_change('value', update_yoffset)
step_slider.on_change('value', update_slider)
start_stop.on_click(toggle_handler)


@gen.coroutine
def update():
    '''update data to be plotted'''
    global started
    global step
    global offset
    if started:
        new_x = source_sin.data['x'][-1]+step
        new_y = np.sin(new_x) + yoffset
        source_sin.stream(dict(x=[new_x], y=[new_y], color=["#bad405"]))
        new_y = np.cos(new_x) + yoffset
        source_cos.stream(dict(x=[new_x], y=[new_y], color=["#666666"]))


# create inputs column
inputs = widgetbox(yoffset_slider, step_slider, start_stop, width=100)

# decide tools to be used
tools = "pan,wheel_zoom,box_zoom,reset,save"  # crosshair
hover = HoverTool(tooltips=[("index", "$index"),
                            ("(x,y)", "($x, $y)")])

# prepare figure
p0 = figure(x_range=[0, 10], y_range=[-1, 1], tools=[tools, hover], plot_width=600)
l0 = p0.circle(x='x', y='y', color='color', source=source_sin)
l1 = p0.circle(x='x', y='y', color='color', source=source_cos)

# add plots
p = gridplot([[p0]], toolbar_location='above')

# add plots to document
doc.add_root(row(inputs, p))
doc.add_periodic_callback(update, 100)
