from flask import Flask, render_template, request
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components

from bokeh.sampledata.periodic_table import elements
from bokeh.transform import dodge, factor_cmap
from bokeh.models import Arrow, OpenHead

app = Flask(__name__)

# Load the Iris Data Set
iris_df = pd.read_csv("data/iris.data",
                      names=["Sepal Length", "Sepal Width", "Petal Length", "Petal Width", "Species"])
feature_names = iris_df.columns[0:-1].values.tolist()


# Create the main plot
def create_figure(current_feature_name, bins):
    
    periods = [str(i) for i in range(0, 18)]
    groups = [str(x) for x in range(0, 19)]
    
    df = elements.copy()
    df = df[:3]
    
    df["atomic mass"] = df["atomic mass"].astype(str)
    df["group"] = df["group"].astype(str)
    df["period"] = [periods[x-1] for x in df.period]
    df = df[df.group != "-"]
    df = df[df.symbol != "Lr"]
    df = df[df.symbol != "Lu"]
    df['period'][0] = 9.5
    df['group'][0] = 6.5
    df['period'][1] = 16.5
    df['group'][1] = 9.5
    df['period'][2] = 9.5
    df['group'][2] = 12.5
    
    df['symbol'][0] = "buy_attr"
    df['symbol'][1] = "comfort_attr"
    df['symbol'][2] = "X_attr"
    
    cmap = {
        "alkali metal"         : "#a6cee3",
        "alkaline earth metal" : "#1f78b4",
        "metal"                : "#d93b43",
        "halogen"              : "#999d9a",
        "metalloid"            : "#e08d49",
        "noble gas"            : "#eaeaea",
        "nonmetal"             : "#f1d4Af",
        "transition metal"     : "#599d7A",
    }
    
    TOOLTIPS = [
        ("Name", "@name"),
        ("Atomic number", "@{atomic number}"),
        ("Atomic mass", "@{atomic mass}"),
        ("Type", "@metal"),
        ("CPK color", "$color[hex, swatch]:CPK"),
        ("Electronic configuration", "@{electronic configuration}"),
    ]
    
    p = figure(title="Periodic Table (omitting LA and AC Series)", plot_width=1000, plot_height=1000,
               x_range=groups, y_range=list(periods),
               tools="hover", toolbar_location=None, tooltips=TOOLTIPS)
    
    p.add_layout(Arrow(end=OpenHead(line_color="firebrick", line_width=4),
                   x_start=9.5, y_start=16.5, x_end=6.5, y_end=9.5))
    p.add_layout(Arrow(end=OpenHead(line_color="firebrick", line_width=4),
                   x_start=9.5, y_start=16.5, x_end=12.5, y_end=9.5))
    
    p.rect("group", "period", 2, 2, source=df, fill_alpha=0.8, legend="metal",
           color=factor_cmap('metal', palette=list(cmap.values()), factors=list(cmap.keys())))
    
    text_props = {"source": df, "text_align": "left", "text_baseline": "middle"}
    
    x = dodge("group", -0.9, range=p.x_range)
    
    r = p.text(x=x, y="period", text="symbol", **text_props)
    r.glyph.text_font_style="bold"
    
    r = p.text(x=x, y=dodge("period", 0.3, range=p.y_range), text="atomic number", **text_props)
    r.glyph.text_font_size="8pt"
    
    r = p.text(x=x, y=dodge("period", -0.35, range=p.y_range), text="name", **text_props)
    r.glyph.text_font_size="5pt"
    
    r = p.text(x=x, y=dodge("period", -0.2, range=p.y_range), text="atomic mass", **text_props)
    r.glyph.text_font_size="5pt"

    p.outline_line_color = None
    p.grid.grid_line_color = "black"
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_standoff = 0
    p.legend.orientation = "vertical"
    p.legend.location = "top_right"
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
@app.route('/q', methods=['GET'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    app.run(port=5000, debug=True)
