cmap = {
    "lens": {
        "ageAttr": "#a6cee3",
        "spectacleAttr": "#1f78b4",
        "astigmaticAttr": "#d93b43",
        "tearAttr": "yellow",
        "classAttr": "#e08d49"
    },
    "cars": {
        "buyingAttr": "red",
        "maintAttr": "beige",
        "doorsAttr": "blue",
        "personsAttr": "green",
        "lug_bootAttr": "brown",
        "safetyAttr": "black",
        "classAttr": "orange"
    }
}

label_to_tr = {
    "lens": {
        "ageAttr": {"1": "Genç", "2": "Orta", "3": "Yaşlı"},
        "spectacleAttr": {"1": "Miyop", "2": "Hipermetrop"},
        "astigmaticAttr": {"1": "Yok", "2": "Var"},
        "tearAttr": {"1": "Az", "2": "Normal"},
        "classAttr": {'-': "Yok", "1": "Sert Lens", "2": "Yumuşak Lens", "3": "Lens Takamaz"}
    },
    "cars": {
        "buyingAttr": {"vhigh": "Çok Yüksek", "high": "Yüksek", "med": "Orta", "low": "Düşük"},
        "maintAttr": {"vhigh": "Çok Yüksek", "high": "Yüksek", "med": "Orta", "low": "Düşük"},
        "doorsAttr": {"2": "2", "3": "3", "4": "4", "5more": "5 ve fazlası"},
        "personsAttr": {"2": "2", "3": "3", "more": "daha fazla"},
        "lug_bootAttr": {"small": "küçük", "med": "orta", "big": "büyük"},
        "safetyAttr": {"low": "düşük", "med": "orta", "high": "yüksek"},
        "classAttr": {"-": "Yok", "unacc": "Zor Satılır", "acc": "Belki Satılır", "good": "Satılır", "vgood": "Kolayca Satılır"}
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
    }
}

def getDictionaries(choose):
    return cmap[choose], label_to_tr[choose], attr_to_turkish[choose], attr_to_children[choose]