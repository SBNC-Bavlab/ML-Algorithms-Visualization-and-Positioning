import pandas as pd
from os.path import join, basename, getsize
import logging
import base64
from bokeh.plotting import figure
from bokeh.transform import dodge, factor_cmap
from bokeh.models import ColumnDataSource, LabelSet, HoverTool, WheelZoomTool, ResetTool, PanTool, Panel, Tabs, Toggle, CustomJS, TapTool
from bokeh.models.widgets import Button, Paragraph, Select, CheckboxGroup
from bokeh.layouts import column, row
from Bokeh.ID3_Decision_Tree.generate_bokeh_data import get_bokeh_data
from math import atan
from Bokeh.Plot.get_data import get_all_colors, set_dataset, set_new_dataset
from Bokeh.Plot.instance import Instance


TOOLTIPS = [
    ("Metod Değeri", "@{nonLeafNodes_stat}"),
    ("Örnek Sayısı", "@{instances}"),
    ("Sonuç", "@{decision}")
]

radio_button_labels = ["gini", "gainRatio"]
tree_mode_labels = ["Basit", "Detaylı"]
arrow_list = {"current": [], "previous": []}
current_label = "gini"
selected_root = ""

plot_width = 1000
plot_height = int(plot_width*950/1400)

rect_width = 2
rect_height = 0.5
circle_radius = 5


def get_new_data_source(df):
    """
    modular data source
    """
    df["nonLeafNodes_stat"] = [str(x) for x in df["nonLeafNodes_stat"]]
    if not df['nonLeafNodes_stat'].dropna().empty:
        df['nonLeafNodes_stat'] = ["-" if i == "None" else str(round(float(i), 3)) for i in df['nonLeafNodes_stat']]
    else:
        df['nonLeafNodes_stat'] = [1]
    df['decision'] = [decision if decision else "-" for decision in df['decision']]
    df["nonLeafNodes_stat"] = df["nonLeafNodes_stat"].fillna(0)
    df["decision"] = ["" + x for x in df["decision"]]


def modify_individual_plot(p, data_source, active_attributes_list, arrow_data_source, root):
    """
    modular plot
    """
    data, width, depth, level_width, acc = get_bokeh_data(current_label, active_attributes_list + [Instance().attr_list[-1]],
                                                          root)
    data = pd.DataFrame.from_dict(data)
    get_new_data_source(data)
    data_source.data = ColumnDataSource(data=data).data

    p.select(name="label").visible = False
    # X and y range calculated
    periods = p.y_range.factors = [str(i) for i in range(0, width + 1)]
    groups = p.x_range.factors = [str(x) for x in range(0, depth + 2)]

    arrow_data, _, _ = draw_arrow(data_source.data, p, width, len(periods), len(groups), level_width, "get_data")
    arrow_data_source.data = ColumnDataSource(data=arrow_data.data).data

    p.title.text = "Karar Ağacı (" + ("Seçtiğiniz " if selected_root else "Algoritmanın Seçtiği ") \
                   + "Kök Nitelikli Hali)" + ("\t\t\t\tTahmin Başarısı (%): "
                                              + str(round(acc * 100, 1)) if acc else "")


def create_figure():
    """
    get data from generate_bokeh_data and create the data source. Define widgets and create the two figures.
    Position the widgets and figures according to rows and columns
    :return: send layout of widgets and plots back to Bokeh
    """
    set_dataset()
    active_attributes_list = [attr for attr in Instance().cmap.keys() if attr != Instance().attr_list[-1]]
    source, width, depth, level_width, acc = get_bokeh_data("gini", active_attributes_list + [Instance().attr_list[-1]],
                                                            selected_root)
    source["nonLeafNodes_stat"] = [str(x) for x in source["nonLeafNodes_stat"]]
    elements = pd.DataFrame.from_dict(source)

    # X and y range calculated
    periods = [str(i) for i in range(0, width+1)]
    groups = [str(x) for x in range(0, depth+2)]

    df = elements.copy()
    get_new_data_source(df)
    data_source = ColumnDataSource(data=df)

    attr_info = Paragraph(text="""
       Nitelikleri seçiniz:
    """, width=200)
    attribute_checkbox = CheckboxGroup(labels=[attr for attr in list(Instance().cmap.keys())
                                               if attr != Instance().attr_list[-1]],
                                       active=[i for i, attr in enumerate(list(Instance().cmap.keys()))])
    apply_changes_button = Button(width=275, label="Değişiklikleri Uygula", button_type="success")
    decision_button = Toggle(width=275, label="Sonuç gösterme", button_type="warning")
    arrow_button = Toggle(width=275, label="Karar değerlerini gösterme", button_type="warning")
    root_select = Select(title="Kök niteliği seçiniz:",
                         options=['Hiçbiri'] + [attr for attr in list(Instance().cmap.keys())[:-1]],
                         value="Hiçbiri")
    method_select = Select(title="Metodu seçiniz:", options=radio_button_labels, value="gini")
    tree_select = Select(title="Ağacın görünümünü seçiniz:", options=tree_mode_labels, value="Basit")
    dataset_select = Select(title="Veri Kümesini Seç:", value="lens", options=["lens", "car"])

    p, arrow_data_source = create_plot(width, level_width, groups, periods, data_source, False, acc)
    p.axis.visible = False

    best_root_plot_data = data_source.data.copy()
    best_root_plot_data_source = ColumnDataSource(data=best_root_plot_data)
    best_root_plot, best_arrow_data_source = create_plot(width, level_width, groups,
                                                         periods, best_root_plot_data_source, True, acc)
    best_root_plot.axis.visible = False

    tab1 = Panel(child=p, title="Yeni ağacınız")
    tab2 = Panel(child=best_root_plot, title="İdeal ağaç")
    tree_tab = Tabs(tabs=[tab1, tab2])



    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """Adapted from https://groups.google.com/a/continuum.io/d/msg/bokeh/EtuMtJI39qQ/ZWuXjBhaAgAJ"""
    """vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv"""
    def new_upload_button(save_path,
                          name="dataset.txt",
                          label="Veri Kümesi Yükleyin"):
        def file_callback(_attr, _old, _new):
            if True:
                raw_contents = file_source.data['contents'][0]
                # remove the prefix that JS adds
                prefix, b64_contents = raw_contents.split(",", 1)
                file_contents = base64.b64decode(b64_contents)
                fname = join(save_path, name)
                with open(fname, "wb") as f:
                    f.write(file_contents)

        file_source = ColumnDataSource({'contents': [], 'name': []})
        file_source.on_change('data', file_callback)

        file_button = Button(width=275, label=label, button_type="success")
        file_button.callback = CustomJS(args=dict(source=file_source), code=_upload_js)
        return file_button, file_source

    _upload_js = """
    function read_file(filename) {
        var reader = new FileReader();
        reader.onload = load_handler;
        reader.onerror = error_handler;
        // readAsDataURL represents the file's data as a base64 encoded string
        reader.readAsDataURL(filename);
    }

    function load_handler(event) {
        var b64string = event.target.result;
        source.data = {'contents' : [b64string], 'name':[input.files[0].name]};
        source.change.emit()
    }

    function error_handler(evt) {
        if(evt.target.error.name == "NotReadableError") {
            alert("Can't read file!");
        }
    }

    var input = document.createElement('input');
    input.setAttribute('type', 'file');
    input.onchange = function(){
        if (window.FileReader) {
            read_file(input.files[0]);
        } else {
            alert('FileReader is not supported in this browser');
        }
    }
    input.click();
    """
    file_button, file_source = new_upload_button("../Bokeh/Data/")
    """^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"""
    """Adapted from https://groups.google.com/a/continuum.io/d/msg/bokeh/EtuMtJI39qQ/ZWuXjBhaAgAJ"""
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



    main_frame = row(column(root_select, attr_info, attribute_checkbox, apply_changes_button,
                            decision_button, arrow_button, dataset_select, tree_select, file_button), tree_tab)

    def update_method_type(_attr, _old, new):
        """
        change method type to be used according to the selected value
        """
        global current_label
        # Method_type -> gini or Gain ratio
        method_type_selected = radio_button_labels[new]
        current_label = method_type_selected

    method_select.on_change("value", update_method_type)

    # Called with respect to change in attributes check-box
    def update_attributes(new):
        """
        create a new active_attributes_list when any of the checkboxes are selected
        """
        global selected_root
        active_attributes_list[:] = []
        for i in new:
            active_attributes_list.append(list(Instance().cmap.keys())[i])
        if selected_root != '' and selected_root not in active_attributes_list:
            apply_changes_button.disabled = True
        else:
            apply_changes_button.disabled = False
    attribute_checkbox.on_click(update_attributes)

    def toggle_mode_set(new):
        """
        toggles settings
        """
        p.select(name="circles").visible = not new
        p.select(name="rectangles").visible = new
        p.select(name="detailed_text").visible = new

        best_root_plot.select(name="circles").visible = not new
        best_root_plot.select(name="rectangles").visible = new
        best_root_plot.select(name="detailed_text").visible = new

        if decision_button.label == "Sonuç gösterme":
            p.select(name="decision_text").visible = not new
            best_root_plot.select(name="decision_text").visible = not new
        decision_button.disabled = new

    def toggle_mode(_attr, _old, new):
        """
        switch between normal and detailed mode
        """
        if new == "Detaylı":
            toggle_mode_set(True)
        else:
            toggle_mode_set(False)

    tree_select.on_change("value", toggle_mode)

    def turn_decision_off(new):
        """
        turn decision text on/off
        """
        if new:
            p.select(name="decision_text").visible = False
            best_root_plot.select(name="decision_text").visible = False
            decision_button.label = "Sonuç göster"
        else:
            p.select(name="decision_text").visible = True
            best_root_plot.select(name="decision_text").visible = True
            decision_button.label = "Sonuç gösterme"

    decision_button.on_click(turn_decision_off)

    def turn_arrow_labels_off(new):
        """
        turn arrow labels on/off
        """
        if new:
            p.select(name="arrowLabels").visible = False
            best_root_plot.select(name="arrowLabels").visible = False
            arrow_button.label = "Karar değerlerini göster"
        else:
            p.select(name="arrowLabels").visible = True
            best_root_plot.select(name="arrowLabels").visible = True
            arrow_button.label = "Karar değerlerini gösterme"
    arrow_button.on_click(turn_arrow_labels_off)

    def source_selected(_attr, _old, _new):
        class_attrs = get_class_attr()
        decision_indices = [[] for x in range(len(class_attrs))]
        for i in range(len(data_source.data['x'])):
            if data_source.data['decision'][i] != "-": # leaf node
                decision_indices[class_attrs.index(data_source.data['decision'][i])]\
                    .append([i, data_source.data['y'][i], data_source.data['x'][i]])
        for i in class_attrs:
            if data_source.data['decision'][data_source.selected.indices[0]] == i:
                selected_class_index = class_attrs.index(i)
        for i in range(len(decision_indices)):
            if i != selected_class_index:
                for j in range(len(decision_indices[i])):
                    x = decision_indices[i][j][2]
                    y = decision_indices[i][j][1]
                    index = decision_indices[i][j][0]
                    a = data_source.data['x'][index]
                    b = data_source.data['y'][index]
                    bool_val_x = a == x
                    bool_val_y = b == y

                    selected = p.select({})
                    selected.visible=False
    data_source.on_change('selected', source_selected)

    def update_root(_attr, _old, new):
        """
        change root attribute to be used for creating a new tree
        """
        global selected_root
        new = root_select.options.index(new)
        method_type_selected = list(Instance().cmap.keys())[new - 1]
        if new == 0:
            selected_root = ''
            apply_changes_button.disabled = False
        elif method_type_selected not in active_attributes_list:
            selected_root = method_type_selected
            apply_changes_button.disabled = True
        else:
            selected_root = method_type_selected
            apply_changes_button.disabled = False
    root_select.on_change('value', update_root)

    def change_dataset(_attr, _old, new):
        """
        use selected dataset for the tree
        """
        global selected_root
        if new == "lens":
            set_new_dataset(new, " ")
        elif new == "car":
            set_new_dataset(new, ",")
        else:
            set_new_dataset("dataset", ",")
        selected_root = ""
        apply_changes()
        attribute_checkbox.labels = [attr for attr in list(Instance().cmap.keys()) if attr != Instance().attr_list[-1]]
        attribute_checkbox.active = [i for i, attr in enumerate(list(Instance().cmap.keys()))]
        root_select.options = ['Hiçbiri'] + [attr for attr in list(Instance().cmap.keys())[:-1]]
        # create_figure()

    dataset_select.on_change('value', change_dataset)

    def apply_changes():
        """
        compute new data source to be used for the new tree. change values of several variables to be used before
        sending them to get_bokeh_data
        """

        modify_individual_plot(p, data_source, active_attributes_list, arrow_data_source, selected_root)
        modify_individual_plot(best_root_plot, best_root_plot_data_source, active_attributes_list,
                               best_arrow_data_source, "")

        apply_changes_button.disabled = False

    apply_changes_button.on_click(apply_changes)

    return main_frame


def create_plot(width, level_width, groups, periods, data_source, is_previous=False, acc=None):
    """
    create glyphs, text and arrows and insert them into the figures
    :param width: width of our tree data
    :param level_width: height of our tree data
    :param groups: groups
    :param periods: periods
    :param data_source: data_source
    :param is_previous: is the customized or ideal tree being created?
    :param acc: accuracy of the tree
    :return: plot p and the arrow data source
    """
    title = "Karar Ağacı " + ("(Algoritmanın Seçtiği Kök Nitelikli Hali)"
                              if is_previous else
                              "(Seçtiğiniz Kök Nitelikli Hali)") + ("\t\t\t\tTahmin Başarısı (%): "
                                                                    + str(round(acc * 100, 1)) if acc else "")
    hover = HoverTool(names=["circles", "rectangles"])
    tap = TapTool(names=["circles", "rectangles"])
    wheel = WheelZoomTool()
    p = figure(title=title, toolbar_location="below", tools=[hover, wheel, ResetTool(), PanTool(), tap],
               plot_width=plot_width, plot_height=plot_height, x_range=groups, y_range=list(periods), tooltips=TOOLTIPS)
    arrow_data_source, arrow, label = draw_arrow(data_source.data, p, width, len(periods), len(groups), level_width)
    p.toolbar.active_scroll = wheel
    p.add_layout(label)
    p.circle("y", "x", radius=circle_radius, radius_units='screen', source=data_source,
             name="circles", legend="attribute_type",
             color=factor_cmap('attribute_type', palette=list(get_all_colors()), factors=Instance().attr_list))
    p.rect("y", "x", rect_width, rect_height, source=data_source, name="rectangles", legend="attribute_type",
           color=factor_cmap('attribute_type', palette=list(get_all_colors()), factors=Instance().attr_list))

    p.select(name="rectangles").visible = False

    # Drawing on the rectangles
    text_props = {"source": data_source, "text_align": "center", "text_baseline": "middle"}

    r = p.text(x="nonLeafNodes_y", y=dodge("nonLeafNodes_x", 0, range=p.x_range),
               name="detailed_text",
               text="nonLeafNodes_stat",
               **text_props)
    r.glyph.text_font_size = "7pt"

    r = p.text(x="y", y=dodge("x", 0.3, range=p.x_range), name="detailed_text", text="attribute_type", **text_props)
    r.glyph.text_font_style = "bold"
    r.glyph.text_font_size = "8pt"

    r = p.text(x="y", y=dodge("x", -0.3, range=p.x_range), name="detailed_text", text="instances", **text_props)
    r.glyph.text_font_size = "8pt"
    r = p.text(x="leafNodes_y", y="leafNodes_x", name="detailed_text", text="decision", **text_props)
    r.glyph.text_font_size = "8pt"

    p.select(name="detailed_text").visible = False

    r = p.text(x="leafNodes_y", text_color="orange", y=dodge("leafNodes_x", -0.4),
               name="decision_text", text="decision", **text_props)
    r.glyph.text_font_size = "8pt"

    # Final settings
    p.outline_line_color = "white"
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_standoff = 0
    p.legend.orientation = "vertical"
    p.legend.location = "top_right"
    return p, arrow_data_source


def draw_arrow(source, p, width, periods_len, groups_len, level_width, mode="draw"):
    """
    draws and returns arrows and the labels. calculates arrow widths from number of instances
    :param source: source
    :param p: plot p to be drawn on
    :param width: width of the tree
    :param periods_len: periods_len
    :param groups_len: groups_len
    :param level_width: height of the tree
    :param mode: when mode isn't draw, it means that the function is being called only for getting the arrow data source
    :return: returns arrow data source, arrows and labels
    """
    arrow_coordinates = {"x_start": [], "x_end": [], "y_start": [], "y_end": [], "x_avg": [], "y_avg": [],
                         "label_name": [], "instances": [], "angle": [], "xs": [], "ys": []}
    arrow = []
    for i in range(width):
        x_offset = 0
        for j in range(level_width[i]):
            offset = sum(level_width[:i])
            if source["attribute_type"][offset + j] != Instance().attr_list[-1]:
                children_names = Instance().attr_values_dict[source["attribute_type"][offset + j]]
                number_of_children = len(children_names)
                for index in range(number_of_children):
                    x_start = source["y"][offset + j]
                    x_end = source["y"][x_offset + index + sum(level_width[: i + 1])]
                    y_start = source["x"][offset + j]
                    y_end = source["x"][index + sum(level_width[: i + 1])]
                    angle = atan((y_end - y_start) / (x_end - x_start) *
                                 (groups_len / periods_len) * (plot_height/plot_width))
                    arrow_coordinates["x_start"].append(x_start)
                    arrow_coordinates["x_end"].append(x_end)
                    arrow_coordinates["y_start"].append(y_start)
                    arrow_coordinates["y_end"].append(y_end)
                    arrow_coordinates["x_avg"].append((x_start + x_end) / 2)
                    arrow_coordinates["angle"].append(angle)
                    arrow_coordinates["y_avg"].append((y_start + y_end) / 2)
                    arrow_coordinates["label_name"].append(children_names[index])
                    arrow_coordinates["instances"].append(source["instances"][index + sum(level_width[: i + 1])])
                x_offset += number_of_children

    arrow_instance_min = min((int(x) for x in arrow_coordinates["instances"]), default=2)
    arrow_instance_max = max((int(x) for x in arrow_coordinates["instances"]), default=1)

    arrow_coordinates["xs"] = [[x_start] for x_start in arrow_coordinates["x_start"]]
    for i in range(len(arrow_coordinates["x_end"])):
        arrow_coordinates["xs"][i] += [arrow_coordinates["x_end"][i]]
    arrow_coordinates["ys"] = [[y_start] for y_start in arrow_coordinates["y_start"]]
    for i in range(len(arrow_coordinates["y_end"])):
        arrow_coordinates["ys"][i] += [arrow_coordinates["y_end"][i]]
    arrow_coordinates["instances"] = [1 + 7 * (int(x) - arrow_instance_min) /
                                      (arrow_instance_max - arrow_instance_min + 1)
                                      for x in arrow_coordinates["instances"]]
    arrow_data_source = ColumnDataSource(data=pd.DataFrame.from_dict(arrow_coordinates))
    if mode == "draw":
        arrow = p.multi_line(line_width="instances", line_alpha=0.7, line_color="darkgray",
                             xs="xs", ys="ys", source=arrow_data_source)
    label = LabelSet(x='x_avg', y='y_avg', angle="angle",
                     name="arrowLabels", text="label_name",
                     text_font_size="8pt", text_color="darkgray", source=arrow_data_source)
    return arrow_data_source, arrow, label
