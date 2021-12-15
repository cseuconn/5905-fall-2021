import shutil

stats = shutil.disk_usage("/")
percentage = stats.used / stats.total

print("Disk usage is ", round(percentage * 100, 0), "%")
