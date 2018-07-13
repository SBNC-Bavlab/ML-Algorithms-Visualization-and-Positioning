import pickle

ageAttr = ["1", "2", "3"]
spectacleAttr = ["1", "2"]
astigmaticAttr = ["1", "2"]
tearAttr = ["1", "2"]

buyingAttr = ["vhigh", "high", "med", "low"]
maintAttr = ["vhigh", "high", "med", "low"]
doorsAttr = ["2", "3", "4", "5more"]
personsAttr = ["2", "4", "more"]
lug_bootAttr = ["small", "med", "big"]
safetyAttr = ["low", "med", "high"]

classAttr = []

choice = "lens"

data_lens = []
test_lens = []


cmap = {
    "lens": {
        "ageAttr": "red",
        "spectacleAttr": "yellow",
        "astigmaticAttr": "blue",
        "tearAttr": "green",
        "classAttr": "orange"
    },
    "cars": {
        "buyingAttr": "red",
        "maintAttr": "yellow",
        "doorsAttr": "blue",
        "personsAttr": "green",
        "lug_bootAttr": "brown",
        "safetyAttr": "black",
        "classAttr": "orange"
    },
    "GoT": {
        "Zengin mi?": "red",
        "Ejderhası var mı?": "beige",
        "Tahtı istiyor mu?": "blue",
        "Saç rengi": "green",
        "Ailesi": "brown"
    }
}

label_to_tr = {
    "lens": {
        "ageAttr": {"1": "Genç", "2": "Orta", "3": "Yaşlı"},
        "spectacleAttr": {"1": "Miyop", "2": "Hipermetrop"},
        "astigmaticAttr": {"1": "Yok", "2": "Var"},
        "tearAttr": {"1": "Az", "2": "Normal"},
        "classAttr": {'-': "-", "1": "Sert Lens", "2": "Yumuşak Lens", "3": "Lens Takamaz"}
    },
    "cars": {
        "buyingAttr": {"vhigh": "Çok Yüksek", "high": "Yüksek", "med": "Orta", "low": "Düşük"},
        "maintAttr": {"vhigh": "Çok Yüksek", "high": "Yüksek", "med": "Orta", "low": "Düşük"},
        "doorsAttr": {"2": "2", "3": "3", "4": "4", "5more": "5 ve fazlası"},
        "personsAttr": {"2": "2", "4": "4", "more": "daha fazla"},
        "lug_bootAttr": {"small": "küçük", "med": "orta", "big": "büyük"},
        "safetyAttr": {"low": "düşük", "med": "orta", "high": "yüksek"},
        "classAttr": {"-": "-", "unacc": "Zor Satılır", "acc": "Belki Satılır",
                      "good": "Satılır", "vgood": "Kolayca Satılır"}
    },
    "GoT": {
        "Zengin mi?": {"Zengin": "Zengin", "Zengin değil": "Zengin değil"},
        "Ejderhası var mı?": {"Var": "Var", "Yok": "Yok"},
        "Tahtı istiyor mu?": {"İstiyor": "İstiyor", "İstemiyor": "İstemiyor"},
        "Saç rengi": {"Sarı": "Sarı", "Siyah": "Siyah", "Beyaz": "Beyaz", "Kızıl": "Kızıl"},
        "Ailesi": {"Lannister": "Lannister", "Stark": "Stark", "White Walker": "White Walker", "Targaryen": "Targaryen"}
    }
}
attr_to_turkish = {
    "lens": {
        "ageAttr": "Yaş",
        "spectacleAttr": "Göz Bozukluğu",
        "astigmaticAttr": "Astigmat",
        "tearAttr": "Göz Yaşı Üretimi",
        "classAttr": "Sonuç"
    },
    "cars": {
        "buyingAttr": "Fiyat",
        "maintAttr": "Bakım Miktarı",
        "doorsAttr": "Kapı Sayısı",
        "personsAttr": "İnsan Kapasitesi",
        "lug_bootAttr": "Bagaj Büyüklüğü",
        "safetyAttr": "Emniyetlilik",
        "classAttr": "Sonuç"
    },
    "GoT": {
        "Zengin mi?": "Zengin mi?",
        "Ejderhası var mı?": "Ejderhası var mı?",
        "Tahtı istiyor mu?": "Tahtı istiyor mu?",
        "Saç rengi": "Saç rengi",
        "Ailesi": "Ailesi"
    }
}

attr_to_children = {
    "lens": {
        "ageAttr": ["1", "2", "3"],
        "spectacleAttr": ["1", "2"],
        "astigmaticAttr": ["1", "2"],
        "tearAttr": ["1", "2"],
        "classAttr": ["1", "2", "3"]
    },
    "cars": {
        "buyingAttr": ["vhigh", "high", "med", "low"],
        "maintAttr":  ["vhigh", "high", "med", "low"],
        "doorsAttr":  ["2", "3", "4", "5more"],
        "personsAttr":  ["2", "4", "more"],
        "lug_bootAttr":  ["small", "med", "big"],
        "safetyAttr":  ["low", "med", "high"],
        "classAttr":  ["unacc", "acc", "good", "vgood"],
    },
    "GoT": {
        "Zengin mi?": {"Zengin", "Zengin değil"},
        "Ejderhası var mı?": {"Var", "Yok"},
        "Tahtı istiyor mu?": {"İstiyor", "İstemiyor"},
        "Saç rengi": {"Sarı", "Siyah", "Beyaz", "Kızıl"},
        "Ailesi": {"Lannister", "Stark", "White Walker", "Targaryen"}
    }
}
all_attrs_list = []
colors = []
for i in cmap.keys():
    for j in cmap[i].keys():
        all_attrs_list.append(j)
    for j in cmap[i].values():
        colors.append(j)
all_attrs_list.remove("classAttr")
colors.remove("orange")

data_set = pickle.load(open('../Bokeh/Data/car.pkl', 'rb'))
data_car = data_set['train']
test_car = data_set['test']

for line in open('../Bokeh/Data/lens.txt'):
    tmp = line.split("  ")
    tmp[-1] = tmp[-1].strip()
    data_lens.append(tmp)
    test_lens.append(tmp)


def get_choice():
    return choice


def set_choice(new):
    global choice
    choice = new


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
    return colors
