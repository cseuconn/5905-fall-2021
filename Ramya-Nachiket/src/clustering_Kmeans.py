import dask_ml.datasets
import dask_ml.cluster
import matplotlib as mlt
mlt.use('Agg')
import matplotlib.pyplot as plt

X, y = dask_ml.datasets.make_blobs(n_samples=10000000,
                                   chunks=1000000,
                                   random_state=0,
                                   centers=3)
X = X.persist()
X
km = dask_ml.cluster.KMeans(n_clusters=3, init_max_iter=2, oversampling_factor=10)
km.fit(X)

#KMeans(init_max_iter=2, n_clusters=3, oversampling_factor=10)
fig, ax = plt.subplots()
ax.scatter(X[::10000, 0], X[::10000, 1], marker='.', c=km.labels_[::10000],
           cmap='viridis', alpha=0.25);
fig.savefig('temp.png')