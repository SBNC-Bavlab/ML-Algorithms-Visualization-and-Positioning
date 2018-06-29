import pandas as pd
from bokeh.io import show
from bokeh.plotting import figure

from bokeh.transform import dodge, factor_cmap
from bokeh.models.widgets import RadioButtonGroup, CheckboxButtonGroup
from bokeh.layouts import column
from Bokeh.ID3_Decision_Tree.generate_bokeh_data import get_bokeh_data

from bokeh.models import Arrow, OpenHead, VeeHead, TeeHead


def draw_arrow(source, p, width, level_width, rect_width, rect_height):
    for i in range(width):
        x_offset = 0
        for j in range(level_width[i]):
            offset = sum(level_width[:i])
            if source["attribute_type"][offset+j] == "personsAttr" or source["attribute_type"][offset+j] == "lug_bootAttr" or source["attribute_type"][offset+j] == "safetyAttr":
                for index in range(3):
                    p.add_layout(Arrow(line_width = 0.5, end = VeeHead(size=10, line_width=0.5), x_start = source["y"][offset+j], y_start = source["x"][offset+j]-rect_height/2, x_end = source["y"][x_offset+index+sum(level_width[:i+1])], y_end = source["x"][index+sum(level_width[:i+1])]+rect_height/2))
                x_offset+=3
            elif source["attribute_type"][offset+j] != "classAttr":
                for index in range(4):
                    p.add_layout(Arrow(line_width = 0.5, end = VeeHead(size=10, line_width=0.5), x_start = source["y"][offset+j], y_start = source["x"][offset+j]-rect_height/2, x_end = source["y"][x_offset+index+sum(level_width[:i+1])], y_end = source["x"][index+sum(level_width[:i+1])]+rect_height/2))
                x_offset+=4

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
    rect_width = 0.95
    rect_height = 0.95

    p.rect("y", "x", rect_width, rect_height, source=df, fill_alpha=0.8, legend="attribute_type",
           color=factor_cmap('attribute_type', palette=list(cmap.values()), factors=list(cmap.keys())))

    text_props = {"source": df, "text_align": "center", "text_baseline": "middle"}

    x = dodge("x", -0.3, range=p.x_range)

    r = p.text(x="y", y=x, text="stat_value", **text_props)
    r.glyph.text_font_size = "7pt"

    r = p.text(x="y", y=dodge("x", 0.3, range=p.x_range), text="attribute_type", **text_props)
    r.glyph.text_font_style = "bold"
    r.glyph.text_font_size = "8pt"
    draw_arrow(source, p, width, level_width, rect_width, rect_height)

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
