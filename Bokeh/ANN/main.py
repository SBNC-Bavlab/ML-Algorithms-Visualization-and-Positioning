from bokeh.plotting import figure
from bokeh.models.widgets import Select, CheckboxGroup, Paragraph, Button
from bokeh.layouts import layout, widgetbox
from Plot.ann_data_instance import ANNData
from bokeh.io import curdoc

all_attrs_list = ["1", "2", "3", "4"]

learning_rate_select = Select(title="Öğrenme Hızını Seçiniz:", options=['1e-5', '1e-3', '0.1', '1'], value="1e-5")
activation_func_select = Select(title="Aktivasyon Fonksiyonunu Seçiniz:", options=['ReLu', 'Tanh', 'Sigmoid'],
                                value='ReLu')
attr_info = Paragraph(text="Nitelikleri seçiniz:")
attribute_checkbox = CheckboxGroup(labels= all_attrs_list,
                                   active=[0, 1, 2, 3])
add_layer_button = Button(label="Katman Ekle", button_type="success")
remove_layer_button = Button(label="Katman Çıkar", button_type="success")
add_node_button = Select(title="Seçtiğiniz Katmana Node Ekle", options=["1", "2", "3", "4"])
remove_node_button = Select(title="Seçtiğiniz Katmandan Node Çıkar", options=["1", "2", "3", "4"])
widgets = widgetbox(learning_rate_select, activation_func_select, attr_info, attribute_checkbox,
                    add_layer_button, remove_layer_button,
                    add_node_button, remove_node_button, sizing_mode="stretch_both")

ANN = ANNData(learning_rate_select.value, activation_func_select.value, layers=[[3]])

p = figure(toolbar_location=None)
p.grid.grid_line_color = None
p.legend.orientation = "vertical"
p.legend.location = "top_right"

visual = layout([[widgets, p]])


def change_learning_rate(_attr, _old, new):
    ANN.update(new, ANN.activation_list, ANN.attr_list, ANN.layers)


learning_rate_select.on_change("value", change_learning_rate)


def change_activation_func(_attr, _old, new):
    ANN.update(ANN.learning_rate, new, ANN.attr_list, ANN.layers)


activation_func_select.on_change("value", change_activation_func)


def change_attributes(new):
    active_attributes_list = []
    for i in new:
        active_attributes_list.append(all_attrs_list[i])
    ANN.update(ANN.learning_rate, ANN.activation_func, active_attributes_list, ANN.layers)


attribute_checkbox.on_click(change_attributes)


def add_layer():
    ANN.update(ANN.learning_rate, ANN.activation_func, ANN.attr_list, ANN.layers+[[3]])
    print(ANN.layers)


add_layer_button.on_click(add_layer)


def remove_layer():
    ANN.update(ANN.learning_rate, ANN.activation_func, ANN.attr_list, ANN.layers[:-1])
    print(ANN.layers)


remove_layer_button.on_click(remove_layer)


def add_node(_attr, _old, new):
    layer = ANN.layers
    new = int(new)
    print(new)
    layer[new-1] += 1
    ANN.update(ANN.learning_rate, ANN.activation_func, ANN.attr_list, layer)
    print(ANN.layers)


add_node_button.on_change("value", add_node)


def remove_node(_attr, _old, new):
    layer = ANN.layers
    layer[int(new)-1] -= 1
    ANN.update(ANN.learning_rate, ANN.activation_func, ANN.attr_list, layer)
    print(ANN.layers)


remove_node_button.on_change("value", remove_node)

curdoc().add_root(visual)
