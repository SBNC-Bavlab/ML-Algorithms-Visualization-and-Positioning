import pandas as pd
from bokeh.io import show
from bokeh.plotting import figure, Figure
from enum import Enum
from time import sleep
from bokeh.transform import dodge, factor_cmap
from bokeh.models import Arrow, OpenHead, VeeHead, ColumnDataSource, Range1d, LabelSet, Title
from bokeh.models.callbacks import CustomJS
from bokeh.models.widgets import RadioButtonGroup, Button, CheckboxButtonGroup, Paragraph
from bokeh.layouts import column, row
from Bokeh.ID3_Decision_Tree.generate_bokeh_data import get_bokeh_data

cmap = {
    "ageAttr": "#a6cee3",
    "spectacleAttr": "#1f78b4",
    "astigmaticAttr": "#d93b43",
    "tearAttr": "yellow",
    "classAttr": "#e08d49"
}
attr_to_children = {"ageAttr": ["1", "2", "3"],
                    "spectacleAttr": ["1", "2"],
                    "astigmaticAttr": ["1", "2"],
                    "tearAttr": ["1", "2"],
                    "classAttr": ["1", "2", "3"]
                    }
TOOLTIPS = [
    ("Nitelik Adı", "@attribute_type"),
    ("Metod Değeri", "@{stat_value}"),
    ("Karar", "@{decision}")
    #        ("Type", "@metal"),
    #        ("CPK color", "$color[hex, swatch]:CPK"),
    #        ("Electronic configuration", "@{electronic configuration}"),
]
# labels for method type radio buttons
radio_button_labels = ["gini", "gainRatio"]
arrow_list = {"current": [], "previous": []}
current_label = ["gini"]
selected_root = [""]

# Create the main plot
def create_figure():
    # Implicitly two attributes is disabled for the beginning
    active_attributes_list = [attr for attr in cmap.keys() if attr != "doorsAttr" and attr != "maintAttr"]
    # method options: gini, gainRatio, informationGain
    source, width, depth, level_width, acc = get_bokeh_data("gini", active_attributes_list, selected_root[0])

    elements = pd.DataFrame.from_dict(source)

    ##X and y range calculated
    periods = [str(i) for i in range(0, 2 * width + 1)]
    groups = [str(x) for x in range(0, depth + 2)]

    df = elements.copy()
    # decimal point rounded to 2
    df['stat_value'] = [round(i, 3) for i in df['stat_value']]
    if not df['nonLeafNodes_stat'].dropna().empty:
        df['nonLeafNodes_stat'] = [round(i, 3) for i in df['nonLeafNodes_stat']]
    else:
        df['nonLeafNodes_stat'] = [1]
    df['decision'] = [decision if decision else "-" for decision in df['decision']]
    df["nonLeafNodes_stat"] = ["Değer: " + str(x) for x in df["nonLeafNodes_stat"]]
    df["decision"] = ["Sonuç: " + x for x in df["decision"]]
    #    df['stat_value'] = [value if value != nan else "-" for value in df['stat_value']]
    #    print(df.last())
    dataSource = ColumnDataSource(data=df)

    # gini or informationGain or gainRatio
    method_type = RadioButtonGroup(width=160, labels=radio_button_labels, active=1)
    # attributes like buyingAttr, personsAttr, ...
    attributes = CheckboxButtonGroup(width=600, labels=list(cmap.keys()),
                                     active=[i for i, attr in enumerate(list(cmap.keys()))
                                             if attr != "doorsAttr" and attr != "maintAttr"])
    # button to apply changes
    button = Button(label="Değişiklikleri Uygula", button_type="success")

    # any attribute type
    root_type = RadioButtonGroup(width=600, labels=['Hiçbiri'] + list(cmap.keys())[:-1], active=0)

    # button to apply changes
    button = Button(label="Değişiklikleri Uygula", button_type="success")

    rect_width = 0.93
    rect_height = 0.93

    p = create_plot(rect_width, rect_height, groups, periods, dataSource, False, acc)

    arrow_data_source, arrow, label = draw_arrow("current", dataSource.data, p, width, level_width, rect_width,
                                                 rect_height)
    p.add_layout(arrow)
    p.add_layout(label)

    attr_info = Paragraph(text="""
       Nitelikleri seçiniz:
    """, width=70)
    method_info = Paragraph(text="""
       Metodu seçiniz:
    """, width=65)
    root_info = Paragraph(text="""
           Kök niteliği seçiniz:
        """, width=70)

    #### Best rooted plot is created here
    best_root_plot_data = dataSource.data.copy()
    best_root_plot_data_source = ColumnDataSource(data=best_root_plot_data)
    best_root_plot = create_plot(rect_width, rect_height, groups, periods, best_root_plot_data_source, True, acc)

    best_arrow_data_source, best_arrow, best_label = draw_arrow("current", best_root_plot_data_source.data,
                                                    best_root_plot, width, level_width, rect_width, rect_height)
    best_root_plot.add_layout(best_arrow)
    best_root_plot.add_layout(best_label)

    ##Add all components into main_frame variable
    main_frame = column(row(attr_info, attributes, method_info, method_type), row(root_info, root_type, button), p, best_root_plot)

    # Called with respect to change in method_type
    def updateMethodType(new):
        ##Method_type -> gini or Gain ratio
        method_type = radio_button_labels[new]
        current_label[0] = method_type

    method_type.on_click(updateMethodType)

    # Called with respect to change in attributes check-box
    def updateAttributes(new):
        active_attributes_list[:] = []
        for i in new:
            active_attributes_list.append(list(cmap.keys())[i])

    attributes.on_click(updateAttributes)

    def updateRoot(new):
        ##Select root manually
        if (new == 0):
            selected_root[0] = ''
        else:
            method_type = list(cmap.keys())[new - 1]
            selected_root[0] = method_type

    root_type.on_click(updateRoot)

    def applyChanges():

        data, width, depth, level_width, acc = get_bokeh_data(current_label[0], active_attributes_list,
                                                              selected_root[0])
        data = pd.DataFrame.from_dict(data)

        data['stat_value'] = [round(i, 3) for i in data['stat_value']]  # decimal point rounded to 2
        if not data['nonLeafNodes_stat'].dropna().empty:
            data['nonLeafNodes_stat'] = [round(i, 3) for i in data['nonLeafNodes_stat']]
        else:
            data['nonLeafNodes_stat'] = [1]
        ##none entries replaced with "-"
        data['decision'] = [decision if decision else "-" for decision in data['decision']]
        data["decision"] = ["Sonuç: " + x for x in data["decision"]]

        dataSource.data = ColumnDataSource(data=data).data

        arrow_data, _, _ = draw_arrow("current", dataSource.data, p, width, level_width, rect_width, rect_height)
        arrow_data_source.data = ColumnDataSource(data=arrow_data.data).data

        ##X and y range calculated
        periods = [str(i) for i in range(0, 2 * width + 1)]
        groups = [str(x) for x in range(0, depth + 2)]
        #        p = create_plot(rect_width, rect_height, groups, periods, dataSource, False, acc)

        p.x_range.factors = groups
        p.y_range.factors = periods

        title = "Karar Ağacı (Seçtiğiniz Kök Nitelikli Hali)" \
                + ("\t\t\t\tTahmin Başarısı (%): " + str(acc * 100) if (acc) else "")

        p.title.text = title
        ####-----------
        ######Refresh best rooted plot
        ####-----------

        data_best, width_best, depth_best, level_width_best, acc_best = get_bokeh_data(current_label[0], active_attributes_list, "")

        # Datasource should be deep copied
        data_best_df = pd.DataFrame.from_dict(data_best)
        data_best_df['stat_value'] = [round(i, 3) for i in data_best_df['stat_value']]  # decimal point rounded to 2
        if not data_best_df['nonLeafNodes_stat'].dropna().empty:
            data_best_df['nonLeafNodes_stat'] = [round(i, 3) for i in data_best_df['nonLeafNodes_stat']]
        else:
            data_best_df['nonLeafNodes_stat'] = [1]
        ##none entries replaced with "-"
        data_best_df['decision'] = [decision if decision else "-" for decision in data_best_df['decision']]
        data_best_df["decision"] = ["Sonuç: " + x for x in data_best_df["decision"]]

        best_root_plot_data_source.data = ColumnDataSource(data=data_best_df).data

        best_arrow_data, _, _ = draw_arrow("current", best_root_plot_data_source.data, best_root_plot,
                                           width_best, level_width_best, rect_width, rect_height)
        best_arrow_data_source.data = ColumnDataSource(data=best_arrow_data.data).data

        ##X and y range calculated
        periods_best = [str(i) for i in range(0, 2 * width_best + 1)]
        groups_best = [str(x) for x in range(0, depth_best + 2)]
        # update best rooted plot
        best_root_plot.x_range.factors = groups_best
        best_root_plot.y_range.factors = periods_best

        title = "Karar Ağacı (Seçtiğiniz Kök Nitelikli Hali)" \
                + ("\t\t\t\tTahmin Başarısı (%): " + str(acc_best * 100) if (acc_best) else "")

        best_root_plot.title.text = title

        animate_outline_color(best_root_plot, 4)

    button.on_click(applyChanges)

    return main_frame


def create_plot(rect_width, rect_height, groups, periods, dataSource, isPrevious=False, acc=None):
    title = "Karar Ağacı " + ("(Algoritmanın Seçtiği Kök Nitelikli Hali)" if (isPrevious) else "(Seçtiğiniz Kök Nitelikli Hali)")+ ("\t\t\t\tTahmin Başarısı (%): " + str(acc * 100) if (acc) else "")
    p = figure(title=title, plot_width=1400, plot_height=500, x_range=groups, y_range=list(periods), tools="hover", toolbar_location=None, tooltips=TOOLTIPS)
    p.rect("y", "x", rect_width, rect_height, source=dataSource, fill_alpha=0.8, legend="attribute_type", color=factor_cmap('attribute_type', palette=list(cmap.values()), factors=list(cmap.keys())))

    #####Drawing on the rectangles####
    text_props = {"source": dataSource, "text_align": "center", "text_baseline": "middle"}

    # r = p.text(x="y", y=dodge("x", -0.3, range=p.x_range), text="stat_value", **text_props)
    # r.glyph.text_font_size = "7pt"


    r = p.text(x="nonLeafNodes_y", y=dodge("nonLeafNodes_x", 0, range=p.x_range), text="nonLeafNodes_stat",
               **text_props)
    r.glyph.text_font_size = "7pt"

    r = p.text(x="y", y=dodge("x", 0.3, range=p.x_range), text="attribute_type", **text_props)
    r.glyph.text_font_style = "bold"
    r.glyph.text_font_size = "8pt"


    r = p.text(x="leafNodes_y", y="leafNodes_x", text="decision", **text_props)
    r.glyph.text_font_size = "8pt"

    r = p.text(x="y", y=dodge("x", -0.3, range=p.x_range), text="instances", **text_props)
    r.glyph.text_font_size = "8pt"
    #
    # r = p.text(x=x, y=dodge("y", -0.2, range=p.y_range), text="atomic mass", **text_props)
    # r.glyph.text_font_size = "5pt"
    ##Final settings##
    p.outline_line_color = "white"
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_standoff = 0
    p.legend.orientation = "vertical"
    p.legend.location = "top_right"
    return p


def draw_arrow(mode, source, p, width, level_width, rect_width, rect_height):
    ##mode is 'current' or 'previous'
    arrow_index = 0  # index for arrow_list array
    arrow_coordinates = {"x_start": [], "x_end": [], "y_start": [], "y_end": [], "x_avg": [], "y_avg": [],
                         "label_name": [], "instances": []}
    for i in range(width):
        x_offset = 0
        for j in range(level_width[i]):
            offset = sum(level_width[:i])
            if source["attribute_type"][offset + j] != "classAttr":
                children_names = attr_to_children[source["attribute_type"][offset + j]]
                number_of_children = len(children_names)
                for index in range(number_of_children):
                    x_start = source["y"][offset + j]
                    y_start = source["x"][offset + j] - rect_height / 2
                    x_end = source["y"][x_offset + index + sum(level_width[: i + 1])]
                    y_end = source["x"][index + sum(level_width[: i + 1])] + rect_height / 2
                    #                    if(True or arrow_index >= len(arrow_list[mode])):
                    arrow_coordinates["x_start"].append(x_start)
                    arrow_coordinates["x_end"].append(x_end)
                    arrow_coordinates["y_start"].append(y_start - 0.06)
                    arrow_coordinates["y_end"].append(y_end + 0.06)
                    arrow_coordinates["x_avg"].append((x_start + x_end) / 2)
                    arrow_coordinates["y_avg"].append((y_start + y_end) / 2)
                    arrow_coordinates["label_name"].append(children_names[index])
                    arrow_coordinates["instances"].append(source["instances"][index + sum(level_width[: i + 1])])
                    arrow_index += 1
                x_offset += number_of_children

    arrow_instance_min = min((int(x) for x in arrow_coordinates["instances"]), default=2)
    arrow_instance_max = max((int(x) for x in arrow_coordinates["instances"]), default=1)

    arrow_coordinates["instances"] = [5 + 5 * (int(x) - arrow_instance_min) / (arrow_instance_max - arrow_instance_min + 1)
                                      for x in arrow_coordinates["instances"]]
    arrow_data_source = ColumnDataSource(data=pd.DataFrame.from_dict(arrow_coordinates))
    arrow = Arrow(line_width="instances", end=OpenHead(size=0, line_width=0.5), line_color="darkgray", line_cap="round",
                  x_start="x_start", y_start="y_start", x_end="x_end", y_end="y_end", source=arrow_data_source)
    label = LabelSet(x="x_avg", y="y_avg", text="label_name",
                     text_font_size="7pt", source=arrow_data_source)
    if (mode == "current"):
        return arrow_data_source, arrow, label
    else:
        p.add_layout(arrow)
        p.add_layout(label)


def animate_outline_color(plot, number, delay=0.5):
    for i in range(number):
        plot.outline_line_color = "red"
        sleep(0.5)
        plot.outline_line_color = "white"
        sleep(0.5)
# show(create_figure())