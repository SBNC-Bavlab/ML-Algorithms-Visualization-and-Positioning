from __future__ import division

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

from bokeh.core.properties import Instance, String
from bokeh.models import ColumnDataSource, LayoutDOM
from bokeh.plotting import figure, show

X = np.array([[5,3],
     [10,15],
     [15,12],
     [24,10],
     [30,45],
     [85,70],
     [71,80],
     [60,7],
     [55,52],
     [80,91]])


kmeans = KMeans(n_clusters=3)
kmeans.fit(X)

print(X)
print(kmeans.cluster_centers_)
print(kmeans.labels_)

cluster_xs = kmeans.cluster_centers_[:, 0]
cluster_ys = kmeans.cluster_centers_[:, 1]
TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"

p = figure(tools=TOOLS)
p.circle(X[:, 0], X[:, 1], size = 5 )
show(p)