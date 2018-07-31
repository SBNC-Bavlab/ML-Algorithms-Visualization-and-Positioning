from __future__ import division
from sklearn.cluster import KMeans
from bokeh.transform import factor_cmap
from bokeh.plotting import figure, show
import pandas as pd

from bokeh.models import ColumnDataSource
from bokeh.layouts import row, column
from bokeh.tile_providers import CARTODBPOSITRON_RETINA
from bokeh.io import curdoc
from bokeh.models.widgets import Slider, Select
import math


def merc_x(lon):
    r_major = 6378137.000
    return r_major*math.radians(lon)


def merc_y(lat):
    if lat > 89.5:
        lat = 89.5
    if lat < -89.5:
        lat=-89.5
    r_major = 6378137.000
    r_minor = 6356752.3142
    temp = r_minor / r_major
    eccent = math.sqrt(1 - temp ** 2)
    phi = math.radians(lat)
    sinphi = math.sin(phi)
    con = eccent * sinphi
    com = eccent / 2
    con = ( (1.0 - con) / (1.0 + con)) ** com
    ts = math.tan((math.pi/2-phi)/2)/con
    y = 0 - r_major*math.log(ts)
    return y


secim_df = pd.read_csv("Data/secim2015.csv")
cmap = {'0': "red", '1': "green", '2': "blue", '3': "orange", '4': "yellow", '5': "pink", '6': "purple"}

vote_results = [[x, y] for x, y in zip(secim_df["GECERSIZ_OY_ORAN"], secim_df["OY_KULLANMA_ORAN"])]
vote_results_map = [[x, y] for x, y in zip(secim_df["BOYLAM"], secim_df["ENLEM"])]

data_source = None
data_source_map = None
center_of_mass_data_source = None

districts = secim_df["ILCE ADI"].tolist()
cities = secim_df["IL ADI"].tolist()
invalid_ratio = secim_df["GECERSIZ_OY_ORAN"].tolist()
turnout = secim_df["OY_KULLANMA_ORAN"].tolist()

columns = ['x', 'y', 'cluster']
select = None


def create_figure():
    global data_source, data_source_map, center_of_mass_data_source, select
    tools = "hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo," \
            "redo,reset,tap,save,box_select,poly_select,lasso_select,"

    kmeans = KMeans(n_clusters=5)
    kmeans.fit(vote_results)

    cluster_xs = kmeans.cluster_centers_[:, 0]
    cluster_ys = kmeans.cluster_centers_[:, 1]

    com_df = pd.DataFrame.from_dict({'x': cluster_xs, 'y': cluster_ys})
    center_of_mass_data_source = ColumnDataSource(data=com_df)

    # Data visualized
    df = pd.DataFrame(columns=columns)

    for index, coords in enumerate(vote_results):
        df = df.append(
            {'x': coords[0], 'y': coords[1], 'cluster': str(kmeans.labels_[index]),
             "ilce_adi": districts[index],
             "il_adi": cities[index],
             "katilim_oran": turnout[index],
             "gecersiz_oran": invalid_ratio[index],
             "color": cmap[str(kmeans.labels_[index])]},
            ignore_index=True)

    p = figure(tools=tools, tooltips=[("İl Adı", "@il_adi"),
                                      ("İlçe Adı", "@ilce_adi"),
                                      ("Geçersiz Oy Oranı", "@gecersiz_oran"),
                                      ("Katılım Oranı", "@katilim_oran")])
    p.title.text = "Seçim"
    data_source = ColumnDataSource(data=pd.DataFrame.from_dict(df))

    p.circle(x='x', y='y', size=5, source=data_source,
             color='color')

    p.rect('x', 'y', 10, 10, width_units="screen", height_units="screen", color="black",
           source=center_of_mass_data_source)

    # Data projected visulized
    df_map = pd.DataFrame(columns=columns)

    for index, coords in enumerate(vote_results_map):
        df_map = df_map.append(
            {'x': merc_x(coords[0]), 'y': merc_y(coords[1]) + 30000, 'cluster': str(kmeans.labels_[index]),
             "ilce_adi": districts[index],
             "il_adi": cities[index],
             "katilim_oran": turnout[index],
             "gecersiz_oran": invalid_ratio[index],
             "color": cmap[str(kmeans.labels_[index])]},
            ignore_index=True)
    p2 = figure(tools=tools, tooltips=[("İl Adı", "@il_adi"),
                                       ("İlçe Adı", "@ilce_adi"),
                                       ("Geçersiz Oy Oranı", "@gecersiz_oran"),
                                       ("Katılım Oranı", "@katilim_oran")],
                x_range=(-2000000, 6000000), y_range=(-1000000, 7000000),
                x_axis_type="mercator", y_axis_type="mercator")
    p2.add_tile(CARTODBPOSITRON_RETINA)

    data_source_map = ColumnDataSource(data=pd.DataFrame.from_dict(df_map))

    p2.circle(x='x', y='y', size=5, source=data_source_map, color='color')

    dataset_slider = Slider(start=1, end=6, value=5, step=1, title="Küme sayısı")

    dataset_slider.on_change('value', change_cluster)

    select = Select(title="Renk:", value="Hiçbiri", options=["Hiçbiri"] + [cmap[str(i)] for i in range(5)])
    select.on_change('value', choose_color)

    return column(dataset_slider, select, row(p, p2))


def choose_color(_attr, _old, new):
    temp_df_map = data_source_map.to_df()

    for i, coords in enumerate(vote_results_map):
        cluster = temp_df_map.at[i, 'cluster']
        temp_df_map.at[i, 'color'] = new if new == cmap[cluster] else "grey" if new != "Hiçbiri" else cmap[cluster]
    data_source_map.data = ColumnDataSource(data=temp_df_map).data


def change_cluster(_attr, _old, new):

    # Adjust colors in Select-Option menu
    select.options = ["Hiçbiri"] + [cmap[str(i)] for i in range(new)]
    # Run the algorithm and reclaculate the colors etc.
    kmeans = KMeans(n_clusters=new)
    kmeans.fit(vote_results)

    temp_df = data_source.to_df()

    for i, coords in enumerate(vote_results):
        cluster = str(kmeans.labels_[i])
        temp_df.at[i, 'x'] = coords[0]
        temp_df.at[i, 'y'] = coords[1]
        temp_df.at[i, 'cluster'] = cluster
        temp_df.at[i, 'color'] = cmap[cluster]

    data_source.data = ColumnDataSource(data=temp_df).data

    temp_df_map = data_source_map.to_df()

    for i, coords in enumerate(vote_results_map):
        cluster = str(kmeans.labels_[i])
        temp_df_map.at[i, 'x'] = merc_x(coords[0])
        temp_df_map.at[i, 'y'] = merc_y(coords[1]) + 30000
        temp_df_map.at[i, 'cluster'] = cluster
        temp_df_map.at[i, 'color'] = cmap[cluster]

    data_source_map.data = ColumnDataSource(data=temp_df_map).data

    cluster_xs = kmeans.cluster_centers_[:, 0]
    cluster_ys = kmeans.cluster_centers_[:, 1]

    temp_com_df = pd.DataFrame.from_dict({'x': cluster_xs, 'y': cluster_ys})
    center_of_mass_data_source.data = ColumnDataSource(data=temp_com_df).data
curdoc().add_root(create_figure())