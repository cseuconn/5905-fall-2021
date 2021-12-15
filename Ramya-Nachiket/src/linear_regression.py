import dask
import dask.dataframe as dd
from dask_jobqueue import SLURMCluster
from dask.distributed import Client
from dask.distributed import performance_report
import numpy as np
import dask.array as da

cluster = SLURMCluster(
    queue='generalsky',
    cores=24,
    memory="50 GB"
)
cluster.scale(jobs=10) 

client = Client(cluster)


beta = np.random.random(100)  # random beta coefficients, no intercept
X = da.random.normal(0, 1, size=(1000000, 100), chunks=(100000, 100))
y = X.dot(beta) + da.random.normal(0, 1, size=1000000, chunks=(100000,))

#print(df_arr)

X, y = dask.persist(X,y)
client.rebalance([X, y])


_, s, _ = np.linalg.svd(2 * X.T.dot(X))
step_size = 1 / s - 1e-8

## define some parameters
max_steps = 100
tol = 1e-8
beta_hat = np.zeros(100) # initial guess


with performance_report(filename = "linear_regression.html"):
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

print(beta_hat)

