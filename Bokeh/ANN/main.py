from bokeh.plotting import figure
from bokeh.models.widgets import Select, Button, Slider, Paragraph, Panel, Tabs
from bokeh.layouts import layout, widgetbox
from Plot.ann_data_instance import ANNData
import ann
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource

learning_rate_select = Select(title="Öğrenme Hızını Seçiniz:", options=['1e-5', '1e-3', '0.01', '0.1', '1'], value="0.01")
activation_func_select = Select(title="Aktivasyon Fonksiyonunu Seçiniz:", options=['ReLu', 'Tanh', 'Sigmoid'],
                                value='ReLu')
add_layer_button = Button(label="Katman Ekle", button_type="success")
remove_layer_select = Select(title="Katman Çıkar:", options=["Seçiniz", "1"])
layer_select = Select(title="Düğüm Eklemek/Çıkarmak İçin Katman Seç:", options=["1"])
add_node_button = Button(label="+", button_type="warning")
remove_node_button = Button(label="-", button_type="warning")
epoch_slider = Slider(start=500, end=50000, value=500, step=500, title="Adım Sayısı Belirle")
play_button = Button(label="Oynat", button_type="success")
play_button_info = Paragraph(text="")
widgets = widgetbox(learning_rate_select, activation_func_select,
                    add_layer_button, remove_layer_select, layer_select,
                    add_node_button, remove_node_button, epoch_slider, play_button, play_button_info,
                    sizing_mode="stretch_both")

ANN = ANNData(learning_rate_select.value, activation_func_select.value, layers=[3, 10], epoch=500)
layer_num = 2
circle_radius = 10

current_layer = "1"


circle_source = ColumnDataSource(data={'x': [], 'y': []})
arrow_source = ColumnDataSource(data={"x_start": [], "x_end": [], "y_start": [], "y_end": [], "xs": [], "ys": []})
loss_source = ColumnDataSource(data={'x': [], 'y': []})
acc_source = ColumnDataSource(data={'x': [], 'y': []})

p = figure(title="Tahmin Başarısı(%): -", toolbar_location=None)
p.outline_line_color = "white"
p.axis.visible = False
p.grid.grid_line_color = None

loss_p = figure(toolbar_location=None)
loss_p.xaxis.axis_label = "Adım Sayısı"
loss_p.yaxis.axis_label = "Zarar Miktarı"
acc_p = figure(toolbar_location=None)
acc_p.xaxis.axis_label = "Adım Sayısı"
acc_p.yaxis.axis_label = "İsabet Miktarı"


circles = p.circle("x", "y", radius=circle_radius, radius_units='screen', source=circle_source, name="circles",
         color="lightseagreen")
p.multi_line(line_alpha=0.7, line_color="darkgray", name="multi_lines", xs="xs", ys="ys", source=arrow_source,
             color="lightseagreen")
loss_p.line('x', 'y', line_width = 2, source = loss_source)
acc_p.line('x', 'y', line_width = 2, source = acc_source)
tab1 = Panel(child=p, title="Yapay Sinir Ağı")
tab2 = Panel(child=loss_p, title="Zarar Grafiği")
tab3 = Panel(child=acc_p, title="İsabet Grafiği")
tree_tab = Tabs(tabs=[tab1, tab2, tab3], width=p.plot_width)
#p.rect(0.5, 5, 0.1, 10, color="lightgray")
#p.add_layout(Arrow(end=NormalHead(fill_color="lightgray", line_color="lightgray"), line_color="lightgray", x_start=0.5, y_start=5, x_end=0.75, y_end=5, line_width=10))
visual = layout([
    [widgets, tree_tab]
])


def apply_changes(layers):
    circle_data = {'x': [], 'y': []}
    arrow_data = {"x_start": [], "x_end": [], "y_start": [], "y_end": [], "xs": [], "ys": []}

    x_offset = 1
    for i in range(len(layers)):
        y_offset = (10 / layers[i]) / 2
        for j in range(layers[i]):
            circle_data['x'].append(x_offset)
            circle_data['y'].append(y_offset)
            y_offset += (10/layers[i])
        x_offset += 1
    circle_source.data = circle_data

    if len(layers) > 1:
        x_offset = 1
        for i in range(len(layers)):
            y_offset = (10 / layers[i]) / 2
            for j in range(layers[i]):
                if i+1 != len(layers):
                    y_next_offset = (10 / layers[i+1]) / 2
                    for index in range(layers[i+1]):
                        arrow_data['x_start'].append(x_offset)
                        arrow_data['x_end'].append(x_offset + 1)
                        arrow_data['y_start'].append(y_offset)
                        arrow_data['y_end'].append(y_next_offset)
                        y_next_offset+= (10/layers[i+1])
                y_offset += (10 / layers[i])
            x_offset += 1

    arrow_data["xs"] = [[x_start] for x_start in arrow_data["x_start"]]
    for i in range(len(arrow_data["x_end"])):
        arrow_data["xs"][i] += [arrow_data["x_end"][i]]
    arrow_data["ys"] = [[y_start] for y_start in arrow_data["y_start"]]
    for i in range(len(arrow_data["y_end"])):
        arrow_data["ys"][i] += [arrow_data["y_end"][i]]

    arrow_source.data = arrow_data


apply_changes(ANN.layers)


def change_learning_rate(_attr, _old, new):
    ANN.update(new, ANN.activation_func, ANN.layers, ANN.epoch)
    apply_changes(ANN.layers)


learning_rate_select.on_change("value", change_learning_rate)


def change_activation_func(_attr, _old, new):
    ANN.update(ANN.learning_rate, new, ANN.layers, ANN.epoch)


activation_func_select.on_change("value", change_activation_func)


def add_layer():
    global layer_num, current_layer
    if len(ANN.layers) == 10:
        return
    layer = ANN.layers[:-1]
    layer += [3]
    layer += [ANN.layers[-1]]
    ANN.update(ANN.learning_rate, ANN.activation_func, layer, ANN.epoch)

    if not layer_select.options:
        add_node_button.disabled = False
        remove_node_button.disabled = False
        current_layer = "1"

    layer_select.options = layer_select.options + [str(layer_num)]
    remove_layer_select.options = remove_layer_select.options + [str(layer_num)]
    layer_num += 1
    apply_changes(ANN.layers)


add_layer_button.on_click(add_layer)


def remove_layer(_attr, _old, new):
    global layer_num
    if new == "Seçiniz":
        return
    elif len(remove_layer_select.options) == 2:
        remove_layer_select.value = "Seçiniz"
        return
    layer = ANN.layers
    layer.pop(int(new)-1)
    ANN.update(ANN.learning_rate, ANN.activation_func, layer, ANN.epoch)
    remove_layer_select.value = "Seçiniz"
    layer_num -= 1

    options = ["Seçiniz"]
    for i in range(layer_num-1):
        options.append(str(i+1))

    layer_select.options = options[1:]
    if not layer_select.options:
        add_node_button.disabled = True
        remove_node_button.disabled = True
    remove_layer_select.options = options
    apply_changes(ANN.layers)


remove_layer_select.on_change("value", remove_layer)


def choose_layer(_attr, _old, new):
    global current_layer
    current_layer = new


layer_select.on_change("value", choose_layer)


def add_node():
    if ANN.layers[int(current_layer)-1] == 10:
        return
    layer = ANN.layers
    layer[int(current_layer)-1] += 1
    ANN.update(ANN.learning_rate, ANN.activation_func, layer, ANN.epoch)
    apply_changes(ANN.layers)


add_node_button.on_click(add_node)


def remove_node():
    if ANN.layers[int(current_layer)-1] == 1:
        return
    layer = ANN.layers
    layer[int(current_layer) - 1] -= 1
    ANN.update(ANN.learning_rate, ANN.activation_func, layer, ANN.epoch)
    apply_changes(ANN.layers)


remove_node_button.on_click(remove_node)


def choose_epoch(_attr, _old, new):
    ANN.update(ANN.learning_rate, ANN.activation_func, ANN.layers, int(new))


epoch_slider.on_change("value", choose_epoch)


def play():
    play_button_info.text = ""
    loss_data = {'x': [], 'y': []}
    acc_data = {'x': [], 'y': []}
    layers = [50*x for x in ANN.layers]
    ann_input = ann.Ann(float(ANN.learning_rate), ANN.activation_func, layers, ANN.epoch)
    testing_acc, loss_arr, acc_arr = ann_input.run_model(play_button, circles)
    play_button_info.text = "Bitti! Zarar ve isabet grafiklerini inceleyin."
    epoch_arr = []
    for i in range(ANN.epoch):
        epoch_arr.append(i)
        loss_arr[i] = int(loss_arr[i])
    loss_data['x'] = epoch_arr
    loss_data['y'] = loss_arr
    acc_data['x'] = epoch_arr
    acc_data['y'] = acc_arr
    loss_source.data = loss_data
    acc_source.data = acc_data
    p.title.text = "Tahmin Başarısı(%): " + str(round(testing_acc * 100))


play_button.on_click(play)


curdoc().add_root(visual)
