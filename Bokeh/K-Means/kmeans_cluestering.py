from __future__ import division
from sklearn.preprocessing import normalize

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from bokeh.transform import factor_cmap
from bokeh.plotting import figure, show
import pandas as pd
from sklearn.datasets.samples_generator import make_blobs
from bokeh.models import ColumnDataSource
from bokeh.layouts import row
"""
districts_df = pd.read_csv("C:/Users/ASUS/Desktop/YSKSecimSonuclari-master/YSKScraper/Data/geocodedAddresses2015.csv")
votes = pd.DataFrame.from_csv("C:/Users/ASUS/Desktop/YSKSecimSonuclari-master/YSKScraper/Data/yskCombined2015.csv")
votes.columns = [col.strip() for col in votes.columns]
# Drop unnecessary columns
votes.drop(["ITIRAZSIZ_GECERLI_OY_SAYISI", "ITIRAZLI_GECERLI_OY_SAYISI", "BIRIM_ID", "MUHTARLIK_ID", "Mahalle / Köy", "SANDIK NO"]
           + [deleted_cols for i, deleted_cols in enumerate(votes.columns) if i > 11], axis=1, inplace=True)
# None values are found and dropped
districts_df = districts_df.replace(' ---', np.nan).dropna()
#Enlem and boylam are casted to float as they will be mean()'ed
districts_df["ENLEM"] = districts_df["ENLEM"].astype(float)
districts_df["BOYLAM"] = districts_df["BOYLAM"].astype(float)
# Unnecesarry col dropped
districts_df.drop(["MAHALLE"], axis=1)
# Unecesarry rows that are mistakenly put by the creator of the dataset, dropped
votes = votes.drop(votes[votes.OY_KULLANAN_SECMEN_SAYISI == " OY_KULLANAN_SECMEN_SAYISI"].index)
# Some attributes are casted to int as sum() function will be applied to them
votes["OY_KULLANAN_SECMEN_SAYISI"] = votes["OY_KULLANAN_SECMEN_SAYISI"].astype(int)
votes["SECMEN_SAYISI"] = votes["SECMEN_SAYISI"].astype(int)
votes["GECERLI_OY_TOPLAMI"] = votes["GECERLI_OY_TOPLAMI"].astype(int)
votes["GECERSIZ_OY_TOPLAMI"] = votes["GECERSIZ_OY_TOPLAMI"].astype(int)
grouped1 = votes.groupby(["İL ADI", "İLÇE ADI"], as_index=False).sum()
grouped2 = districts_df.groupby(["İL ADI", "İLÇE ADI"], as_index=False).mean()
final_df = pd.merge(grouped1, grouped2[["İLÇE ADI", "ENLEM", "BOYLAM"]], on=["İLÇE ADI"])
# Final adjustments
final_df["İLÇE ADI"] = [row.strip() for row in final_df["İLÇE ADI"]]
final_df["İL ADI"] = [row.strip() for row in final_df["İL ADI"]]
final_df["GECERSIZ_OY_ORAN"] = [invalid / (invalid + valid) * 100
                                for valid, invalid
                                in zip(final_df["GECERLI_OY_TOPLAMI"], final_df["GECERSIZ_OY_TOPLAMI"])]
final_df["OY_KULLANMA_ORAN"] = [used / total_voter * 100
                                for used, total_voter
                                in zip(final_df["OY_KULLANAN_SECMEN_SAYISI"], final_df["SECMEN_SAYISI"])]
final_df.to_csv("Data/secim2015.csv", sep=",", header=True, index=False, encoding="utf-8")
"""

secim_df = pd.read_csv("Data/secim2015.csv")
print(secim_df)
X = [[x, y] for x, y in zip(secim_df["GECERSIZ_OY_ORAN"], secim_df["OY_KULLANMA_ORAN"])]


def create_figure(X):
    tools = "hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo," \
            "redo,reset,tap,save,box_select,poly_select,lasso_select,"
    p = figure(tools=tools, tooltips=[("İl Adı", "@il_adi"),
                                      ("İlçe Adı", "@ilce_adi"),
                                      ("Geçersiz Oy Oranı", "@gecersiz_oran"),
                                      ("Katılım Oranı", "@katilim_oran")])
    p.title.text = "Seçim"
    kmeans = KMeans(n_clusters=7)
    kmeans.fit(X)

    districts = secim_df["İLÇE ADI"].tolist()
    cities = secim_df["İL ADI"].tolist()
    invalid_ratio = secim_df["GECERSIZ_OY_ORAN"].tolist()
    turnout = secim_df["OY_KULLANMA_ORAN"].tolist()

    cluster_xs = kmeans.cluster_centers_[:, 0]
    cluster_ys = kmeans.cluster_centers_[:, 1]

    columns = ['x','y','cluster']
    df = pd.DataFrame(columns=columns)

    for index, coords in enumerate(X):
        df = df.append({'x': coords[0], 'y': coords[1], 'cluster': str(kmeans.labels_[index]),
                        "ilce_adi": districts[index],
                        "il_adi": cities[index],
                        "katilim_oran": turnout[index],
                        "gecersiz_oran": invalid_ratio[index]},
                       ignore_index=True)

    cmap = {'0': "red", '1': "green", '2': "blue", '3': "orange", '4': "yellow"}

    dataSource = ColumnDataSource(data=pd.DataFrame.from_dict(df))

    p.circle(x='x', y='y', size=5, source=dataSource,  color=factor_cmap('cluster', palette=list(cmap.values()), factors=list(cmap.keys())))

    p.rect(cluster_xs, cluster_ys, 10, 10, width_units = "screen", height_units = "screen", color="black")
    return p

p = create_figure(X)
show(row(p))
