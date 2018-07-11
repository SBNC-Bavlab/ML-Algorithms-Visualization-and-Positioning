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
        "classAttr": {'-': "Yok", "1": "Sert Lens", "2": "Yumuşak Lens", "3": "Lens Takamaz"}
    },
    "cars": {
        "buyingAttr": {"vhigh": "Çok Yüksek", "high": "Yüksek", "med": "Orta", "low": "Düşük"},
        "maintAttr": {"vhigh": "Çok Yüksek", "high": "Yüksek", "med": "Orta", "low": "Düşük"},
        "doorsAttr": {"2": "2", "3": "3", "4": "4", "5more": "5 ve fazlası"},
        "personsAttr": {"2": "2", "4": "4", "more": "daha fazla"},
        "lug_bootAttr": {"small": "küçük", "med": "orta", "big": "büyük"},
        "safetyAttr": {"low": "düşük", "med": "orta", "high": "yüksek"},
        "classAttr": {"-": "Yok", "unacc": "Zor Satılır", "acc": "Belki Satılır", "good": "Satılır", "vgood": "Kolayca Satılır"}
    },
    "GoT": {
        "Zengin mi?": {"Zengin" : "Zengin", "Zengin değil" : "Zengin değil"},
        "Ejderhası var mı?": {"Var" : "Var", "Yok" : "Yok"},
        "Tahtı istiyor mu?": {"İstiyor" : "İstiyor", "İstemiyor" : "İstemiyor"},
        "Saç rengi": {"Sarı" : "Sarı", "Siyah" : "Siyah", "Beyaz" : "Beyaz", "Kızıl" : "Kızıl"},
        "Ailesi": {"Lannister" : "Lannister", "Stark" : "Stark", "White Walker" : "White Walker", "Targaryen" : "Targaryen"}
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
allAttrsList = []
colors=[]
for i in cmap.keys():
    for j in cmap[i].keys():
        allAttrsList.append(j)
    for j in cmap[i].values():
        colors.append(j)
allAttrsList.remove("classAttr")
colors.remove("orange")

def getDictionaries(choose):
    return cmap[choose], label_to_tr[choose], attr_to_turkish[choose], attr_to_children[choose]

def getAttrsList():
    return allAttrsList

def getAllColors():
    return colors