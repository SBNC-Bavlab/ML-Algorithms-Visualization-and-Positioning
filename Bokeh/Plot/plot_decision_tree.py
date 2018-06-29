import pandas as pd
from bokeh.io import show
from bokeh.plotting import figure

from bokeh.transform import dodge, factor_cmap
from bokeh.models.widgets import RadioButtonGroup, CheckboxButtonGroup
from bokeh.layouts import column
from Bokeh.ID3_Decision_Tree.generate_bokeh_data import get_bokeh_data

# Create the main plot
def create_figure():
    # method options: gini, gainRatio, informationGain
    source, width, depth, level_width = get_bokeh_data("gini")

    elements = pd.DataFrame.from_dict(source)
    periods = [str(i) for i in range(0, 2*width+1)]
    groups = [str(x) for x in range(0, depth+2)]

    df = elements.copy()
    df['stat_value'] = [round(i, 3) for i in df['stat_value']]

    cmap = {
        "buyingAttr": "#a6cee3",
        "personsAttr": "#1f78b4",
        "lug_bootAttr": "#d93b43",
        "safetyAttr": "#999d9a",
        "classAttr": "#e08d49"
    }

    TOOLTIPS = [
        ("Attribute Name", "@attribute_type"),
        ("Stat Value", "@{stat_value}")
#        ("Atomic mass", "@{atomic mass}"),
#        ("Type", "@metal"),
#        ("CPK color", "$color[hex, swatch]:CPK"),
#        ("Electronic configuration", "@{electronic configuration}"),
    ]
    
    method_type = RadioButtonGroup(labels=["gini", "gainRatio", "informationGain"], active=0)
    attributes = CheckboxButtonGroup(labels = list(cmap.keys()), active = [i for i, _ in enumerate(cmap.keys())])
    p = figure(title="Periodic Table (omitting LA and AC Series)", plot_width=1400, plot_height=630,
               x_range=groups, y_range=list(periods),
               tools="hover", toolbar_location=None, tooltips= TOOLTIPS)
    def update(new):
        print(new)
        data, width, depth, level_width = get_bokeh_data(new)

    elements = pd.DataFrame.from_dict(source)
    periods = [str(i) for i in range(0, 2*width+1)]
    groups = [str(x) for x in range(0, depth+2)]

    df = elements.copy()
    df['stat_value'] = [round(i, 2) for i in df['stat_value']]       
    method_type.on_click(update)


    p.rect("y", "x", 0.95, 0.95, source=df, fill_alpha=0.8, legend="attribute_type",
           color=factor_cmap('attribute_type', palette=list(cmap.values()), factors=list(cmap.keys())))

    text_props = {"source": df, "text_align": "center", "text_baseline": "middle"}

    x = dodge("x", -0.3, range=p.x_range)
    
    r = p.text(x="y", y=x, text="stat_value", **text_props)
    r.glyph.text_font_size = "7pt"
    
    r = p.text(x="y", y=dodge("x", 0.3, range=p.x_range), text="attribute_type", **text_props)
    r.glyph.text_font_style = "bold"
    r.glyph.text_font_size = "8pt"
    
    # r = p.text(x=x, y=dodge("y", -0.35, range=p.y_range), text="name", **text_props)
    # r.glyph.text_font_size = "5pt"
    #
    # r = p.text(x=x, y=dodge("y", -0.2, range=p.y_range), text="atomic mass", **text_props)
    # r.glyph.text_font_size = "5pt"
    
    p.outline_line_color = None
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_standoff = 0
    p.legend.orientation = "vertical"
    p.legend.location = "top_right"
    return column(method_type, attributes, p)
show(create_figure())