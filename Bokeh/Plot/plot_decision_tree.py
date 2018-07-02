import pandas as pd
from bokeh.io import show
from bokeh.plotting import figure, Figure
from enum import Enum
from time import sleep
from bokeh.transform import dodge, factor_cmap
from bokeh.models import Arrow, VeeHead, ColumnDataSource, Range1d, LabelSet, Title
from bokeh.models.callbacks import CustomJS
from bokeh.models.widgets import RadioButtonGroup, Button, CheckboxButtonGroup, Paragraph
from bokeh.layouts import column, row
from Bokeh.ID3_Decision_Tree.generate_bokeh_data import get_bokeh_data

cmap = {
        "buyingAttr": "#a6cee3",
        "personsAttr": "#1f78b4",
        "lug_bootAttr": "#d93b43",
        "maintAttr": "yellow",
        "doorsAttr": "magenta",
        "safetyAttr": "#999d9a",
        "classAttr": "#e08d49"
    }
attr_to_children = {"personsAttr" : ["2", "4", "more"], 
                    "lug_bootAttr" : ["small", "med", "big"], 
                    "safetyAttr" : ["low", "med", "high"], 
                    "maintAttr" : ["vhigh", "high", "med", "low"], 
                    "doorsAttr" : ["2", "3", "4", "5more"], 
                    "buyingAttr" : ["vhigh", "high", "med", "low"]}
TOOLTIPS = [
        ("Nitelik Adı", "@attribute_type"),
        ("Metod Değeri", "@{stat_value}"),
        ("Karar", "@{decision}")
#        ("Type", "@metal"),
#        ("CPK color", "$color[hex, swatch]:CPK"),
#        ("Electronic configuration", "@{electronic configuration}"),
    ]
#labels for method type radio buttons
radio_button_labels = ["gini", "gainRatio"]
arrow_list = {"current": [], "previous": []}
current_label= ["gainRatio"]
previous_plot = []
##All of the attribute index hard coded
##enum for method i.e gini, gainRatio
class Method(Enum):
    GINI = 0
    GAIN = 1

# Create the main plot
def create_figure():
    
    #Implicitly two attributes is disabled for the beginning
    active_attributes_list = [attr for attr in cmap.keys() if attr != "doorsAttr" and attr != "maintAttr"]
    # method options: gini, gainRatio, informationGain
    source, width, depth, level_width, acc = get_bokeh_data("gainRatio", active_attributes_list)

    elements = pd.DataFrame.from_dict(source)
    
    ##X and y range calculated
    periods = [str(i) for i in range(0, 2*width+1)]
    groups = [str(x) for x in range(0, depth+2)]

    df = elements.copy()
    #decimal point rounded to 2
    df['stat_value'] = [round(i, 3) for i in df['stat_value']]
    df['decision'] = [decision if decision else "-" for decision in df['decision']]
    
#    df['stat_value'] = [value if value != nan else "-" for value in df['stat_value']]
#    print(df.last())
    dataSource = ColumnDataSource(data = df)

    
    #gini or informationGain or gainRatio
    method_type = RadioButtonGroup(width = 160, labels = radio_button_labels, active=1) 
    #attributes like buyingAttr, personsAttr, ...
    attributes = CheckboxButtonGroup(width = 600, labels = list(cmap.keys()),
                                     active = [i for i, attr in enumerate(list(cmap.keys())) 
                                             if attr != "doorsAttr" and attr != "maintAttr"])
    #button to apply changes   
    button = Button(label="Değişiklikleri Uygula", button_type="success")
    
    rect_width = 0.93
    rect_height = 0.93
    
    p = create_plot(rect_width, rect_height, groups, periods, dataSource, False, acc)
    
    arrow_data_source, arrow, label = draw_arrow("current", dataSource.data, p, width, level_width, rect_width, rect_height)
    p.add_layout(arrow)
    p.add_layout(label)
    
    attr_info = Paragraph(text="""
       Nitelikleri seçiniz:
    """, width = 70)
    method_info = Paragraph(text="""
       Metodu seçiniz:
    """, width = 65)
    ##Add all components into main_frame variable
    main_frame = column(row(attr_info, attributes, method_info, method_type, button), p)
    #Called with respect to change in method_type
    def updateMethodType(new):
            print(new)
            ##Method_type -> gini or Gain ratio
            method_type = radio_button_labels[new]
            current_label[0] = method_type
            
    method_type.on_click(updateMethodType)
    
    #Called with respect to change in attributes check-box
    def updateAttributes(new):
        active_attributes_list[:] = []         
        for i in new:
            active_attributes_list.append(list(cmap.keys())[i])
        print(new)
        
    attributes.on_click(updateAttributes)
    
    def applyChanges():
        
        data, width, depth, level_width, acc = get_bokeh_data(current_label[0], active_attributes_list)        
        data = pd.DataFrame.from_dict(data)
        
        data['stat_value'] = [round(i, 3) for i in data['stat_value']] #decimal point rounded to 2
        ##none entries replaced with "-"
        data['decision'] = [decision if decision else "-" for decision in data['decision']]
        
        dataSource.data = ColumnDataSource(data=data).data
        
        arrow_data, _, _ = draw_arrow("current", dataSource.data, p, width, level_width, rect_width, rect_height)
        arrow_data_source.data = ColumnDataSource(data=arrow_data.data).data
        
        ##X and y range calculated
        periods = [str(i) for i in range(0, 2*width+1)]
        groups = [str(x) for x in range(0, depth+2)]
#        p = create_plot(rect_width, rect_height, groups, periods, dataSource, False, acc)
        
        p.x_range.factors = groups
        p.y_range.factors = periods
        
        title = "Karar Ağacı (Yeni)" \
                                   + ("\t\t\t\tTahmin Başarısı (%): " + str(acc * 100) if(acc) else "")

        p.title.text = title
                
        ##Below code means if the previous already laid out pop it and add new current as previous
        ##This code is a precaution against the case that there is only one figure
        if(isinstance(main_frame.children[-2], Figure)):
            main_frame.children.pop()
        main_frame.children.append(previous_plot[0])
        #animate the entrance of previous tree
        
#        main_frame.children.pop()
        #update previous
        #Datasource should be deep copied
        deep_copied_data = dataSource.data.copy()
        temp_dataSource = ColumnDataSource(data = deep_copied_data)
        previous = create_plot(rect_width, rect_height, groups, periods, temp_dataSource, True, acc)
#        draw_arrow("current", dataSource.data, p, width, level_width, rect_width, rect_height)
        animate_outline_color(previous_plot[0], 4)
        previous_plot[0] = previous
        draw_arrow("previous", temp_dataSource.data, previous, width, level_width, rect_width, rect_height)

            
    button.on_click(applyChanges)
    print(main_frame.children)
    
    #Datasource should be deep copied
    deep_copied_data = dataSource.data.copy()
    temp_dataSource = ColumnDataSource(data = deep_copied_data)
    previous = create_plot(rect_width, rect_height, groups, periods, temp_dataSource, True, acc)
    draw_arrow("previous", temp_dataSource.data, previous, width, level_width, rect_width, rect_height)
    previous_plot.append(previous)
    return main_frame

def create_plot(rect_width, rect_height, groups, periods, dataSource, isPrevious = False, acc = None):
    title = "Karar Ağacı " + ("(Eski)" if(isPrevious) else "(Yeni)") \
                                   + ("\t\t\t\tTahmin Başarısı (%): " + str(acc * 100) if(acc) else "")
    p = figure(title=title,\
               plot_width=1400, plot_height=500,\
               x_range=groups, y_range=list(periods),\
               tools="hover", toolbar_location=None, tooltips= TOOLTIPS)\
    
    p.rect("y", "x", rect_width, rect_height, source=dataSource, fill_alpha=0.8, legend="attribute_type",
           color=factor_cmap('attribute_type', palette=list(cmap.values()), factors=list(cmap.keys())))    
    
    #####Drawing on the rectangles####
    text_props = {"source": dataSource, "text_align": "center", "text_baseline": "middle"}

    r = p.text(x="y", y=dodge("x", -0.3, range=p.x_range), text="stat_value", **text_props)
    r.glyph.text_font_size = "7pt"
    
    r = p.text(x="y", y=dodge("x", 0.3, range=p.x_range), text="attribute_type", **text_props)
    r.glyph.text_font_style = "bold"
    r.glyph.text_font_size = "8pt"
    
    r = p.text(x="y", y=dodge("x", 0, range=p.x_range), text="decision", **text_props)
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
    arrow_index = 0 #index for arrow_list array    
    arrow_coordinates = {"x_start" : [], "x_end" : [], "y_start" : [], "y_end" : [], "x_avg" : [], "y_avg" : [], "label_name" : []}
    for i in range(width):
        x_offset = 0
        for j in range(level_width[i]):
            offset = sum(level_width[:i])
            if source["attribute_type"][offset+j] != "classAttr":
                children_names = attr_to_children[source["attribute_type"][offset+j]]
                number_of_children = len(children_names)
                for index in range(number_of_children):
                    x_start = source["y"][offset + j]
                    y_start = source["x"][offset + j] - rect_height / 2
                    x_end = source["y"][x_offset + index + sum(level_width[: i + 1])]
                    y_end = source["x"][index + sum(level_width[: i + 1])] + rect_height / 2
#                    if(True or arrow_index >= len(arrow_list[mode])):
                    arrow_coordinates["x_start"].append(x_start)
                    arrow_coordinates["x_end"].append(x_end)
                    arrow_coordinates["y_start"].append(y_start)
                    arrow_coordinates["y_end"].append(y_end)
                    arrow_coordinates["x_avg"].append((x_start + x_end) / 2)
                    arrow_coordinates["y_avg"].append((y_start + y_end) / 2)
                    arrow_coordinates["label_name"].append(children_names[index])
                    print(arrow_index, " was here1")
                    arrow_index += 1
                x_offset += number_of_children
    arrow_data_source = ColumnDataSource(data=pd.DataFrame.from_dict(arrow_coordinates))
    arrow = Arrow(line_width = 0.5, end = VeeHead(size=10, line_width=0.5), 
                                  x_start = "x_start", y_start = "y_start", x_end = "x_end", y_end = "y_end", source = arrow_data_source)
    label = LabelSet(x="x_avg", y="y_avg", text = "label_name",
                                 text_font_size = "7pt", source = arrow_data_source)
    if(mode == "current"):
        return arrow_data_source, arrow, label
    else:
        p.add_layout(arrow) 
        p.add_layout(label)    
def animate_outline_color(plot, number, delay = 0.5):
     for i in range(number):
        plot.outline_line_color = "red"
        sleep(0.5)
        plot.outline_line_color = "white"
        sleep(0.5)
#show(create_figure())