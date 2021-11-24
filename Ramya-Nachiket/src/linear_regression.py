import dask
import dask.dataframe as dd
from dask_jobqueue import SLURMCluster
from dask.distributed import Client
import numpy as np

cluster = SLURMCluster(
    queue='generalsky',
    project="ramya-nachiket-cloud-systems",
    cores=24,
    memory="50 GB"
)
cluster.scale(jobs=10) 

client = Client(cluster)

filename = "E:/Cloud-Systems/Ramya-Nachiket/data/Linear Regression - Sheet1.csv"

df = dd.read_csv(filename)

#print(df)

X, y = dask.persist(df['X'], df['y'])
client.rebalance([X, y])

_, s, _ = np.linalg.svd(2 * X.T.dot(X))
step_size = 1 / s - 1e-8

## define some parameters
max_steps = 100
tol = 1e-8
beta_hat = np.zeros(100) # initial guess

for k in range(max_steps):
    Xbeta = X.dot(beta_hat)
    func = ((y - Xbeta)**2).sum()
    gradient = 2 * X.T.dot(Xbeta - y)

    ## Update
    obeta = beta_hat
    beta_hat = beta_hat - step_size * gradient
    new_func = ((y - X.dot(beta_hat))**2).sum()
    beta_hat, func, new_func = dask.compute(beta_hat, func, new_func)  # <--- Dask code

    ## Check for convergence
    change = np.absolute(beta_hat - obeta).max()

    if change < tol:
        break



