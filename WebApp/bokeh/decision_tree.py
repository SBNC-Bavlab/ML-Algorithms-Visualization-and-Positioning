import pandas as pd
from bokeh.io import show
from bokeh.plotting import figure
from bokeh.embed import components

from bokeh.transform import dodge, factor_cmap
from bokeh.models import Arrow, OpenHead

from ID3_Decision_Tree.generate_bokeh_data import get_bokeh_data

# Create the main plot
def create_figure():
    # method options: gini, gainRatio, informationGain
    source, width, depth = get_bokeh_data("gini")

    elements = pd.DataFrame.from_dict(source)
    periods = [str(i) for i in range(0, width+2)]
    groups = [str(x) for x in range(0, depth+10)]

    df = elements.copy()


    cmap = {
        "buyingAttr": "#a6cee3",
        "personsAttr": "#1f78b4",
        "lug_bootAttr": "#d93b43",
        "safetyAttr": "#999d9a",
        "classAttr": "#e08d49"
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
               tools="hover", toolbar_location=None, tooltips=[])

    p.rect("y", "x", 0.8, 0.8, source=df, fill_alpha=0.8, legend="attribute_type",
           color=factor_cmap('attribute_type', palette=list(cmap.values()), factors=list(cmap.keys())))

    text_props = {"source": df, "text_align": "left", "text_baseline": "middle"}

    x = dodge("y", -0.9, range=p.x_range)
    #
    # r = p.text(x=x, y="y", text="stat_value", **text_props)
    # r.glyph.text_font_style = "bold"
    #
    # r = p.text(x=x, y=dodge("y", 0.3, range=p.y_range), text="atomic number", **text_props)
    # r.glyph.text_font_size = "8pt"
    #
    # r = p.text(x=x, y=dodge("y", -0.35, range=p.y_range), text="name", **text_props)
    # r.glyph.text_font_size = "5pt"
    #
    # r = p.text(x=x, y=dodge("y", -0.2, range=p.y_range), text="atomic mass", **text_props)
    # r.glyph.text_font_size = "5pt"

    p.outline_line_color = None
    p.grid.grid_line_color = "black"
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_standoff = 0
    p.legend.orientation = "vertical"
    p.legend.location = "top_right"
    return p

show(create_figure())