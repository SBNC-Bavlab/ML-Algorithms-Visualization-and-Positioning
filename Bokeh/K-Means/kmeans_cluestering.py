
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

X = np.array([[5,3,4],
     [10,15,2],
     [15,12,3],
     [24,10,5],
     [30,45,6],
     [85,70,7],
     [71,80,2],
     [60,7,8],
     [55,52,61],
     [80,91,4]])


kmeans = KMeans(n_clusters=3)
kmeans.fit(X)

print(X)
print(kmeans.cluster_centers_)
print(kmeans.labels_)

cluster_xs = kmeans.cluster_centers_[:, 0]
cluster_ys = kmeans.cluster_centers_[:, 1]
plt.scatter(X[:,0],X[:,1], X[:,2], c=kmeans.labels_, cmap='rainbow')
plt.scatter(cluster_xs, cluster_ys, color = 'black')
plt.show()