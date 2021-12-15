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
sp = dask_ml.cluster.SpectralClustering(n_clusters=8, eigen_solver=None, 
random_state=None, n_init=10, gamma=1.0, affinity='rbf', n_neighbors=10, 
eigen_tol=0.0, assign_labels='kmeans', degree=3, coef0=1, kernel_params=None,
 n_jobs=1, n_components=100, persist_embedding=False, kmeans_params=None)


fig, ax = plt.subplots()
ax.scatter(X[::10000, 0], X[::10000, 1], marker='.', c=sp.labels_[::10000],
           cmap='viridis', alpha=0.25);
fig.savefig('temp.png')