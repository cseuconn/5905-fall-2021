import redis
import shutil
import yaml
import socket

r = redis.Redis(host='localhost', port=6379)
stats = shutil.disk_usage("/")
percentage = stats.used / stats.total

with open('/code/front-envoy.yaml') as f:
    dict = yaml.full_load(f)
    key = dict["static_resources"]["clusters"][0]["health_checks"][0]["custom_health_check"]["typed_config"]["key"]
    
    r.set(key, int(round(percentage * 100, 0)))

r.set("server", socket.gethostbyname(socket.gethostname()))
