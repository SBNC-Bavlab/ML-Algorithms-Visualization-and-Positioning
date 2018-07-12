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
#X, y = make_blobs()
df = pd.read_csv("../Data/customer.csv")

xs = df['Milk'].values
ys = df['Delicassen'].values
X = np.array(list(zip(xs, ys)))
X = normalize(X)
def create_figure(random_cluster = True):
    TOOLS = "hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"
    p = figure(tools=TOOLS)

    if random_cluster:
        p.title.text = "A"
        kmeans = KMeans(n_clusters=2)
    else:
        p.title.text = "B"
        kmeans = KMeans(n_clusters=4)#init=np.array([[5,5],[5,5],[5,5]]))
    kmeans.fit(X)

    cluster_xs = kmeans.cluster_centers_[:, 0]
    cluster_ys = kmeans.cluster_centers_[:, 1]

    columns = ['x','y','cluster']
    df = pd.DataFrame(columns=columns)

    for  index, coords in enumerate(X):
        df = df.append({'x': coords[0], 'y': coords[1], 'cluster': str(kmeans.labels_[index])}, ignore_index=True)

    cmap = {'0': "red", '1': "green", '2': "blue", '3': "orange", '4': "beige"}

    dataSource = ColumnDataSource(data=pd.DataFrame.from_dict(df))

    p.circle(x='x', y='y', size=5, source=dataSource,  color=factor_cmap('cluster', palette=list(cmap.values()), factors=list(cmap.keys())))

    p.rect(cluster_xs, cluster_ys, 5, 5, width_units = "screen", height_units = "screen", color="black")


    return p;
p = create_figure()
#p2 = create_figure(False)
show(row(p))