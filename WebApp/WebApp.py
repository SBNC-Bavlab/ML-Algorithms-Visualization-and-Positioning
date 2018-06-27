from flask import Flask, render_template, request
import pandas as pd
from bokeh.charts import Histogram
from bokeh.plotting import figure
from bokeh.embed import components

app = Flask(__name__)

# Load the Iris Data Set
iris_df = pd.read_csv("data/iris.data",
                      names=["Sepal Length", "Sepal Width", "Petal Length", "Petal Width", "Species"])
feature_names = iris_df.columns[0:-1].values.tolist()


# Create the main plot
def create_figure(current_feature_name, bins):
    #p = figure(plot_width=600, plot_height=400)
    #p.vbar(x = "asd")
     p = Histogram(iris_df, current_feature_name, title=current_feature_name, color='Species',
                   bins=bins, legend='top_right', width=600, height=400)
    
     # Set the x axis label
     p.xaxis.axis_label = current_feature_name
    
     # Set the y axis label
     p.yaxis.axis_label = 'Count'
     return p


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