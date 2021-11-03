import dask.dataframe as dd


filename = "E:/Cloud-Systems/Ramya-Nachiket/data/Linear Regression - Sheet1.csv"

df = dd.read_csv(filename)

print(df.head())