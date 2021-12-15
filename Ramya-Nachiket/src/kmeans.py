import sklearn
from sklearn import *

data, labels = sklearn.datasets.make_blobs(n_samples=1000, n_features=416, centers=20)
#print(data)
k_means = sklearn.cluster.KMeans(n_clusters=10,init='k-means++', max_iter=3).fit(data)
print(k_means.labels_)