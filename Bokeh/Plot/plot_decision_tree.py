import pandas as pd
from bokeh.io import show
from bokeh.plotting import figure, Figure
from time import sleep
from bokeh.transform import dodge, factor_cmap
from bokeh.models import Arrow, OpenHead, VeeHead, ColumnDataSource, Range1d, LabelSet, Title, HoverTool
from bokeh.models.callbacks import CustomJS
from bokeh.models.widgets import RadioButtonGroup, Button, CheckboxButtonGroup, Paragraph, Dropdown, Select
from bokeh.layouts import column, row
from Bokeh.ID3_Decision_Tree.generate_bokeh_data import get_bokeh_data
from math import sqrt, pi, atan, cos, sin
from Bokeh.Plot.dictionaries import getDictionaries, getAttrsList, getAllColors
from Bokeh.Plot.getChoice import getChoice, setChoice


cmap, label_to_tr, attr_to_turkish, attr_to_children = getDictionaries(getChoice())
allAttrsList = getAttrsList()
TOOLTIPS = [
    ("Metod Değeri", "@{nonLeafNodes_stat}"),
    ("Örnek Sayısı", "@{instances}")
    #        ("Type", "@metal"),
    #        ("CPK color", "$color[hex, swatch]:CPK"),
    #        ("Electronic configuration", "@{electronic configuration}"),
]
# labels for method type radio buttons
radio_button_labels = ["gini", "gainRatio"]
tree_mode_labels = ["Basit", "Detaylı"]
arrow_list = {"current": [], "previous": []}
current_label = ["gini"]
selected_root = [""]


# Create the main plot
def create_figure():
    # Implicitly two attributes is disabled for the beginning
    active_attributes_list = [attr for attr in cmap.keys() if attr != "classAttr"]
    # method options: gini, gainRatio, informationGain
    source, width, depth, level_width, acc = get_bokeh_data("gini", active_attributes_list + ["classAttr"],
                                                            selected_root[0])
    elements = pd.DataFrame.from_dict(source)

    ##X and y range calculated
    max_arg = max(2*width+1, depth+2)
    periods = [str(i) for i in range(0, 2*width+1)]
    groups = [str(x) for x in range(0, depth+2)]

    df = elements.copy()
    # decimal point rounded to 2
    #df['stat_value'] = [round(i, 3) for i in df['stat_value']]
    if not df['nonLeafNodes_stat'].dropna().empty:
        df['nonLeafNodes_stat'] = [round(i, 3) for i in df['nonLeafNodes_stat']]
    else:
        df['nonLeafNodes_stat'] = [1]
    df['decision'] = [decision if decision else "-" for decision in df['decision']]
    df["nonLeafNodes_stat"] = ["" + str(x) for x in df["nonLeafNodes_stat"]]
    df["decision"] = ["" + x for x in df["decision"]]
    df["decision_tr"] = [label_to_tr["classAttr"]["" + x]for x in df["decision"]]
    df['attribute_type_tr'] = [attr_to_turkish[attr] for attr in df['attribute_type']]
    #    df['stat_value'] = [value if value != nan else "-" for value in df['stat_value']]
    #    print(df.last())
    print(df)
    dataSource = ColumnDataSource(data=df)

    # gini or informationGain or gainRatio
    method_type = RadioButtonGroup(width=200, labels=radio_button_labels, active=1)
    # attributes like buyingAttr, personsAttr, ...
    attributes = CheckboxButtonGroup(width=700, labels=[attr_to_turkish[attr] for attr in list(cmap.keys()) if attr != "classAttr"],
                                     active=[i for i, attr in enumerate(list(cmap.keys()))])
    # button to apply changes
    button = Button(label="Değişiklikleri Uygula", button_type="success")

    # any attribute type
    root_type = RadioButtonGroup(width=700,
                                 labels=['Hiçbiri'] + [attr_to_turkish[attr] for attr in list(cmap.keys())[:-1]],
                                 active=0)

    tree_mode = RadioButtonGroup(width=200, labels=tree_mode_labels, active=0)
    menu = [("Lens Verileri", "item_1"), ("Araba Verileri", "item_2")]
    # button to apply changes
    button = Button(label="Değişiklikleri Uygula", button_type="success")
    dropdown = Select(title="Veri Kümesini Seç:", value="lens", options=["lens", "araba"])

    rect_width = 0.7
    rect_height = 0.9
    circle_radius = 0.2

    p, arrow_data_source = create_plot(circle_radius, rect_width, rect_height, width, level_width, groups, periods, dataSource, False, acc)
    p.axis.visible=False


    attr_info = Paragraph(text="""
       Nitelikleri seçiniz:
    """, width=70)
    method_info = Paragraph(text="""
       Metodu seçiniz:
    """, width=70)
    root_info = Paragraph(text="""
           Kök niteliği seçiniz:
        """, width=70)
    tree_mode_info = Paragraph(text="""
           Ağacın Detayını Seçiniz:
        """, width=70)

    #### Best rooted plot is created here
    best_root_plot_data = dataSource.data.copy()
    best_root_plot_data_source = ColumnDataSource(data=best_root_plot_data)
    best_root_plot, best_arrow_data_source = create_plot(circle_radius, rect_width, rect_height, width, level_width, groups, periods, best_root_plot_data_source, True, acc)
    best_root_plot.axis.visible=False
    #best_arrow_data_source, best_arrow, best_label = draw_arrow(best_root_plot_data_source.data,
    #                                                best_root_plot, width, level_width, circle_radius, rect_height)
    #best_root_plot.add_layout(best_arrow)
    #best_root_plot.add_layout(best_label)


    ##Add all components into main_frame variable
    main_frame = column(row(attr_info, attributes, method_info, method_type, button), row(root_info, root_type, tree_mode_info, tree_mode, dropdown), row(p, best_root_plot))

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
        if (selected_root[0] != '' and selected_root[0] not in active_attributes_list):
            button.disabled = True
        else:
            button.disabled = False
    attributes.on_click(updateAttributes)

    def toggleMode(new):
        if(new):
            circles = p.select(name="circles")
            circles.visible=False
            rectangles = p.select(name="rectangles")
            rectangles.visible=True

            circles = best_root_plot.select(name="circles")
            circles.visible=False
            rectangles = best_root_plot.select(name="rectangles")
            rectangles.visible=True

            p.select(name="detailed_text").visible=True
            p.select(name="decision_text").visible=False

            best_root_plot.select(name="detailed_text").visible=True
            best_root_plot.select(name="decision_text").visible=False
        else:
            circles = p.select(name="circles")
            circles.visible=True
            rectangles = p.select(name="rectangles")
            rectangles.visible=False

            circles = best_root_plot.select(name="circles")
            circles.visible=True
            rectangles = best_root_plot.select(name="rectangles")
            rectangles.visible=False

            p.select(name="detailed_text").visible=False
            p.select(name="decision_text").visible=True

            best_root_plot.select(name="detailed_text").visible=False
            best_root_plot.select(name="decision_text").visible=True


    tree_mode.on_click(toggleMode)

    def updateRoot(new):
        ##Select root manually
        method_type = list(cmap.keys())[new - 1]
        if (new == 0):
            selected_root[0] = ''
            button.disabled = False;
        elif (method_type not in active_attributes_list):
            selected_root[0] = method_type
            button.disabled = True;
            print("Bu attribute zaten kapali")
        else:
            selected_root[0] = method_type
            button.disabled = False;
    root_type.on_click(updateRoot)
    def changeDataset(attr, old, new):
        if dropdown.value == "lens":
             setChoice("lens")
        else:
            setChoice("cars")
        applyChanges()
        attributes.labels = [attr_to_turkish[attr] for attr in list(cmap.keys()) if attr != "classAttr"]
        attributes.active = [i for i, attr in enumerate(list(cmap.keys()))]
        root_type.labels = ['Hiçbiri'] + [attr_to_turkish[attr] for attr in list(cmap.keys())[:-1]]

    dropdown.on_change('value', changeDataset)

    def applyChanges():
        global cmap, label_to_tr, attr_to_turkish, attr_to_children
        cmap, label_to_tr, attr_to_turkish, attr_to_children = getDictionaries(getChoice())

        data, width, depth, level_width, acc = get_bokeh_data(current_label[0], active_attributes_list  + ["classAttr"], selected_root[0])

        data = pd.DataFrame.from_dict(data)
        #data['stat_value'] = [round(i, 3) for i in data['stat_value']]  # decimal point rounded to 2
        if not data['nonLeafNodes_stat'].dropna().empty:
            data['nonLeafNodes_stat'] = [round(i, 3) for i in data['nonLeafNodes_stat']]
        else:
            data['nonLeafNodes_stat'] = [1]
        ##none entries replaced with "-"
        data['decision'] = [decision if decision else "-" for decision in data['decision']]
        data["decision"] = ["" + x for x in data["decision"]]
        data["decision_tr"] = [label_to_tr["classAttr"]["" + x] for x in data["decision"]]
        data['attribute_type_tr'] = [attr_to_turkish[attr] for attr in data['attribute_type']]
        dataSource.data = ColumnDataSource(data=data).data

        arrow_data, _, _ = draw_arrow(dataSource.data, p, width, level_width, circle_radius, rect_height, "get_data")
        arrow_data_source.data = ColumnDataSource(data=arrow_data.data).data

        ##X and y range calculated
        periods = [str(i) for i in range(0, 2 * width + 1)]
        groups = [str(x) for x in range(0, depth + 2)]
        #        p = create_plot(rect_width, rect_height, groups, periods, dataSource, False, acc)

        max_arg = max(2 * width + 1, depth + 2)
        p.y_range.factors = [str(i) for i in range(0, 2 * width + 1)]
        p.x_range.factors = [str(x) for x in range(0, depth + 2)]

        title = "Karar Ağacı (Seçtiğiniz Kök Nitelikli Hali)" \
                + ("\t\t\t\tTahmin Başarısı (%): " + str(round(acc * 100, 1)) if (acc) else "")

        p.title.text = title
        ####-----------
        ######Refresh best rooted plot
        ####-----------

        data_best, width_best, depth_best, level_width_best, acc_best = get_bokeh_data(current_label[0], active_attributes_list + ["classAttr"], "")

        # Datasource should be deep copied
        data_best_df = pd.DataFrame.from_dict(data_best)
        #data_best_df['stat_value'] = [round(i, 3) for i in data_best_df['stat_value']]  # decimal point rounded to 2
        if not data_best_df['nonLeafNodes_stat'].dropna().empty:
            data_best_df['nonLeafNodes_stat'] = [round(i, 3) for i in data_best_df['nonLeafNodes_stat']]
        else:
            data_best_df['nonLeafNodes_stat'] = [1]
        ##none entries replaced with "-"
        data_best_df['decision'] = [decision if decision else "-" for decision in data_best_df['decision']]
        data_best_df["decision"] = ["" + x for x in data_best_df["decision"]]
        data_best_df["decision_tr"] = [label_to_tr["classAttr"]["" + x] for x in data_best_df["decision"]]
        data_best_df['attribute_type_tr'] = [attr_to_turkish[attr] for attr in data_best_df['attribute_type']]
        best_root_plot_data_source.data = ColumnDataSource(data=data_best_df).data

        best_arrow_data, _, _ = draw_arrow(best_root_plot_data_source.data, best_root_plot,
                                           width_best, level_width_best, circle_radius, rect_height, "get_data")
        best_arrow_data_source.data = ColumnDataSource(data=best_arrow_data.data).data

        ##X and y range calculated
        max_arg = max(2 * width + 1, depth + 2)
        periods_best = [str(i) for i in range(0, 2 * width + 1)]
        groups_best = [str(x) for x in range(0, depth + 2)]
        # update best rooted plot
        best_root_plot.x_range.factors = groups_best
        best_root_plot.y_range.factors = periods_best

        title = "Karar Ağacı (Algoritmanın Seçtiği Kök Nitelikli Hali)" \
                + ("\t\t\t\tTahmin Başarısı (%): " + str(round(acc_best * 100, 1)) if (acc_best) else "")

        best_root_plot.title.text = title
        button.disabled = True
        tree_mode.disabled = True
        button.disabled = False
        tree_mode.disabled = False

    button.on_click(applyChanges)

    return main_frame


def create_plot(circle_radius, rect_width, rect_height, width, level_width, groups, periods, dataSource, isPrevious=False, acc=None):
    title = "Karar Ağacı " + ("(Algoritmanın Seçtiği Kök Nitelikli Hali)" if (isPrevious) else "(Seçtiğiniz Kök Nitelikli Hali)")+ ("\t\t\t\tTahmin Başarısı (%): " + str(round(acc * 100, 1)) if (acc) else "")
    p = figure(title=title, plot_width=650, plot_height=441, x_range=groups, y_range=list(periods), tools="hover", toolbar_location=None, tooltips=TOOLTIPS)
    arrow_data_source, arrow, label = draw_arrow(dataSource.data, p, width, level_width, circle_radius,
                                                 rect_height)
    p.add_layout(label)
    p.circle("y", "x", radius=circle_radius, source=dataSource, name="circles", legend="attribute_type_tr", color=factor_cmap('attribute_type', palette=list(getAllColors()), factors=allAttrsList))
    print(p.legend)
    p.rect("y", "x", rect_width, rect_height, source=dataSource, name="rectangles", legend="attribute_type_tr",
           color=factor_cmap('attribute_type', palette=list(getAllColors()), factors=allAttrsList))
    rectangles = p.select(name="rectangles")
    rectangles.visible = False

    #####Drawing on the rectangles####
    text_props = {"source": dataSource, "text_align": "center", "text_baseline": "middle"}

    r = p.text(x="nonLeafNodes_y", y=dodge("nonLeafNodes_x", 0, range=p.x_range),
               name="detailed_text",
               text="nonLeafNodes_stat",
               **text_props)
    r.glyph.text_font_size = "7pt"
    #
    r = p.text(x="y", y=dodge("x", 0.3, range=p.x_range), name="detailed_text", text="attribute_type_tr", **text_props)
    r.glyph.text_font_style = "bold"
    r.glyph.text_font_size = "8pt"
    #
    #
    #
    r = p.text(x="y", y=dodge("x", -0.3, range=p.x_range), name="detailed_text", text="instances", **text_props)
    r.glyph.text_font_size = "8pt"
    r = p.text(x="leafNodes_y", y="leafNodes_x", name="detailed_text", text="decision_tr", **text_props)
    r.glyph.text_font_size = "8pt"

    p.select(name="detailed_text").visible = False

    #r = p.text(x="y", y=dodge("x", -0.3, range=p.x_range), text="stat_value", **text_props)
    #r.glyph.text_font_size = "7pt"

    r = p.text(x="leafNodes_y", text_color="orange", y=dodge("leafNodes_x", -0.4), name="decision_text", text="decision_tr", **text_props)
    r.glyph.text_font_size = "8pt"

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
    return p, arrow_data_source


def draw_arrow(source, p, width, level_width, circle_radius, rect_height, mode="draw"):
    ##mode is 'current' or 'previous'
    arrow_index = 0  # index for arrow_list array
    arrow_coordinates = {"x_start": [], "x_end": [], "y_start": [], "y_end": [], "x_avg": [], "y_avg": [],
                         "label_name": [], "instances": [], "angle": [], "xs": [], "ys": [], "label_name_tr": []}
    for i in range(width):
        x_offset = 0
        for j in range(level_width[i]):
            offset = sum(level_width[:i])
            if source["attribute_type"][offset + j] != "classAttr":
                children_names = attr_to_children[source["attribute_type"][offset + j]]
                number_of_children = len(children_names)
                for index in range(number_of_children):
                    distanceBetweenX = source["y"][offset + j] - source["y"][x_offset + index + sum(level_width[: i + 1])]
                    distanceBetweenY = source["x"][offset + j] - source["x"][index + sum(level_width[: i + 1])]
                    distanceBetweenNodes = sqrt(distanceBetweenX**2 + distanceBetweenY**2)

                    x_start = source["y"][offset + j] \
                              #- distanceBetweenX*circle_radius/distanceBetweenNodes
                    x_end = source["y"][x_offset + index + sum(level_width[: i + 1])] \
                            #+ distanceBetweenX*circle_radius/distanceBetweenNodes
                    y_start = source["x"][offset + j] \
                              #- distanceBetweenY*circle_radius/distanceBetweenNodes
                    y_end = source["x"][index + sum(level_width[: i + 1])] \
                            #+ distanceBetweenY*circle_radius/distanceBetweenNodes
                    angle = atan((y_end - y_start) / (x_end - x_start))
                    text_length = len(children_names[index])
                    #if(True or arrow_index >= len(arrow_list[mode])):
                    arrow_coordinates["x_start"].append(x_start)
                    arrow_coordinates["x_end"].append(x_end)
                    arrow_coordinates["y_start"].append(y_start)
                    arrow_coordinates["y_end"].append(y_end)
                    arrow_coordinates["x_avg"].append((x_start + x_end) / 2 - text_length * cos(angle) / 2 * 0.65)
                    arrow_coordinates["angle"].append(angle)
                    arrow_coordinates["y_avg"].append((y_start + y_end) / 2 - text_length * sin(angle) / 2 * 0.65)
                    arrow_coordinates["label_name"].append(children_names[index])
                    arrow_coordinates["label_name_tr"].append(label_to_tr[source['attribute_type'][offset + j]][children_names[index]])
                    arrow_coordinates["instances"].append(source["instances"][index + sum(level_width[: i + 1])])
                    arrow_index += 1
                x_offset += number_of_children

    arrow_instance_min = min((int(x) for x in arrow_coordinates["instances"]), default=2)
    arrow_instance_max = max((int(x) for x in arrow_coordinates["instances"]), default=1)

    arrow_coordinates["xs"] = [[x_start] for x_start in arrow_coordinates["x_start"]]
    for i in range(len(arrow_coordinates["x_end"])):
        arrow_coordinates["xs"][i]+=[arrow_coordinates["x_end"][i]]
    arrow_coordinates["ys"] = [[y_start] for y_start in arrow_coordinates["y_start"]]
    for i in range(len(arrow_coordinates["y_end"])):
        arrow_coordinates["ys"][i]+=[arrow_coordinates["y_end"][i]]

    arrow_coordinates["instances"] = [1 + 7 * (int(x) - arrow_instance_min) / (arrow_instance_max - arrow_instance_min + 1)
                                      for x in arrow_coordinates["instances"]]
    arrow_data_source = ColumnDataSource(data=pd.DataFrame.from_dict(arrow_coordinates))
    if mode=="draw":
        arrow = p.multi_line(line_width="instances", line_alpha=1, line_color="darkgray",
                      xs = "xs", ys="ys", source=arrow_data_source)
    else:
        arrow = []
    label = LabelSet(x=dodge("x_avg", 0.0), angle = "angle", y=dodge("y_avg", 0.0), text="label_name_tr",
                     text_font_size="10pt", text_color="gray", source=arrow_data_source)
    return arrow_data_source, arrow, label

def animate_outline_color(plot, number, delay=0.5):
    for i in range(number):
        plot.outline_line_color = "red"
        sleep(0.5)
        plot.outline_line_color = "white"
        sleep(0.5)
# show(create_figure())