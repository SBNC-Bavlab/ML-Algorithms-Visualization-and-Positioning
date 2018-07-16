import pickle
from Bokeh.Plot.instance import Instance


all_attrs_list = []
color = ["red", "yellow", "blue", "green", "brown", "black", "orange"]


def set_dataset():
    data = []
    attr_values = []
    attr_list = []
    cmap = {}
    for i, line in enumerate(open('../Bokeh/Data/lens.txt')):
        if i == 0:
            attr_list = line.split(" ")
            attr_list[-1] = attr_list[-1].strip()
            cmap = {attr: color[j] for j, attr in enumerate(attr_list)}
            attr_values = [set() for _ in attr_list]
        else:
            datum = line.split(" ")
            datum[-1] = datum[-1].strip()
            data.append(datum)
            for j, val in enumerate(data[-1]):
                attr_values[j].add(val)
    attr_values_dict = dict((attr, list(attr_values[i])) for i, attr in enumerate(attr_list))
    attr_dict = dict((attr, (i, attr)) for i, attr in enumerate(attr_list))
    instance = Instance(data, attr_values, attr_list, attr_values_dict, attr_dict, cmap)


def set_active_attr(active_attr_list):
    """ Set attributes that are in use"""
    # clear the list
    attr_names_list = []
    # fill again
    for attr in active_attr_list:
        attr_names_list.append(attr)
    return attr_names_list


def get_train_set():
    global classAttr
    classAttr = get_class_attr()
    train = data_lens if get_choice() == "lens" else data_car
    return train, classAttr


def get_test_set():
    global classAttr
    classAttr = get_class_attr()
    test = test_lens if get_choice() == "lens" else test_car
    return test, classAttr


def get_new_values():
    """ Set attribute and values according to the data set"""
    global classAttr
    if get_choice() == "cars":
        classAttr = ["unacc", "acc", "good", "vgood"]
    else:
        classAttr = ["1", "2", "3"]

    attr_names_list = [
        "ageAttr",
        "spectacleAttr",
        "astigmaticAttr",
        "tearAttr",
        "classAttr"
    ] if get_choice() == "lens" else [
        "buyingAttr",
        "maintAttr",
        "doorsAttr",
        "personsAttr",
        "lug_bootAttr",
        "safetyAttr",
        "classAttr"
    ]

    attr_dictionary = {
        "ageAttr": (0, ageAttr),
        "spectacleAttr": (1, spectacleAttr),
        "astigmaticAttr": (2, astigmaticAttr),
        "tearAttr": (3, tearAttr),
        "classAttr": (4, classAttr)
    } if get_choice() == "lens" else {
        "buyingAttr": (0, buyingAttr),
        "maintAttr": (1, maintAttr),
        "doorsAttr": (2, doorsAttr),
        "personsAttr": (3, personsAttr),
        "lug_bootAttr": (4, lug_bootAttr),
        "safetyAttr": (5, safetyAttr),
        "classAttr": (6, classAttr)
    }
    return attr_names_list, attr_dictionary


def get_class_attr():
    get_new_values()
    return classAttr


def modify_new_values(tmp_attr_names, attr_names_list, attr_dictionary):
    """ Set new data set attributes """
    new_attr_names = []
    for attr in attr_names_list:
        if attr in tmp_attr_names:
            new_attr_names.append(attr)
        else:
            attr_dictionary.pop(attr)
    attr_names_list = new_attr_names
    return attr_names_list, attr_dictionary


def get_dictionaries(choose):
    return cmap[choose], label_to_tr[choose], attr_to_turkish[choose], attr_to_children[choose], all_attrs_list


def get_all_colors():
    return color
