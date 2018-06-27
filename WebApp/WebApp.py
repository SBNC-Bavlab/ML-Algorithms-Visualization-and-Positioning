from flask import Flask, render_template, request
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components

import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval
from bokeh.palettes import Spectral8

app = Flask(__name__)

# Load the Iris Data Set
iris_df = pd.read_csv("data/ks-projects-201801.csv",
                      names=["Sepal Length", "Sepal Width", "Petal Length", "Petal Width", "Species"])
feature_names = iris_df.columns[0:-1].values.tolist()


# Create the main plot
def create_figure(current_feature_name, bins):
    #p = figure(plot_width=600, plot_height=400)
    #p.vbar(x = "asd")
#     p = Histogram(iris_df, current_feature_name, title=current_feature_name, color='Species',
#                   bins=bins, legend='top_right', width=600, height=400)
#    
#     # Set the x axis label
#     p.xaxis.axis_label = current_feature_name
#    
#     # Set the y axis label
#     p.yaxis.axis_label = 'Count'
    N = 8
    node_indices = list(range(N))

    plot = figure(title="Graph Layout Demonstration", x_range=(-1.1,1.1), y_range=(-1.1,1.1),
                  tools="", toolbar_location=None)

    graph = GraphRenderer()

    graph.node_renderer.data_source.add(node_indices, 'index')
    graph.node_renderer.data_source.add(Spectral8, 'color')
    graph.node_renderer.glyph = Oval(height=0.1, width=0.2, fill_color="color")

    graph.edge_renderer.data_source.data = dict(
        start=[0]*N,
        end=node_indices)

    ### start of layout code
    circ = [i*2*math.pi/8 for i in node_indices]
    x = [math.cos(i) for i in circ]
    y = [math.sin(i) for i in circ]
    graph_layout = dict(zip(node_indices, zip(x, y)))
    graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

    ### Draw quadratic bezier paths
    def bezier(start, end, control, steps):
        return [(1-s)**2*start + 2*(1-s)*s*control + s**2*end for s in steps]

    xs, ys = [], []
    sx, sy = graph_layout[0]
    steps = [i/100. for i in range(100)]
    for node_index in node_indices:
        ex, ey = graph_layout[node_index]
        xs.append(bezier(sx, ex, 0, steps))
        ys.append(bezier(sy, ey, 0, steps))
    graph.edge_renderer.data_source.data['xs'] = xs
    graph.edge_renderer.data_source.data['ys'] = ys

    plot.renderers.append(graph)
    return plot


# Index page
@app.route('/')
def index():
    # Determine the selected feature
    current_feature_name = request.args.get("feature_name")
    if current_feature_name == None:
        current_feature_name = "Sepal Length"

    # Create the plot
    plot = create_figure(current_feature_name, 5)

    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    return render_template("index.html", script=script, div=div,
                           feature_names=feature_names, current_feature_name=current_feature_name)


# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    app.run(port=5000, debug=True)
