from flask import Flask
from flask import request
from flask import make_response
import os
import requests
import socket
import sys
import shutil

app = Flask(__name__)

TRACE_HEADERS_TO_PROPAGATE = [
    'X-Ot-Span-Context',
    'X-Request-Id',

    # Zipkin headers
    'X-B3-TraceId',
    'X-B3-SpanId',
    'X-B3-ParentSpanId',
    'X-B3-Sampled',
    'X-B3-Flags',

    # Jaeger header (for native client)
    "uber-trace-id",

    # SkyWalking headers.
    "sw8"
]


@app.route('/service/<service_number>')
def hello(service_number):
    return (
        'Hello from behind Envoy (service {})! hostname: {} resolved'
        'hostname: {}\n'.format(
            os.environ['SERVICE_NAME'], socket.gethostname(),
            socket.gethostbyname(socket.gethostname())))

@app.route('/health_check')
def health_check():
    stats = shutil.disk_usage("/")
    percentage = stats.used / stats.total
    threshold = float(request.headers['disk-usage-threshold'])

    if not threshold:
        return ('Disk usage threshold not sent. Please send the disk usage threshold as the HTTP header \'disk-usage-threshold\'')

    threshold_met = percentage < threshold
    message = "Hello! The host {} has used {:.2%} percent of it\'s total disk space.\n "
    
    if threshold_met:
        message = message + "This is less than the threshold of {:.0%} and therefore this host is not degraded!"
    else:
        message = message + "This is greater than the threshold of {:.0%} and therefore this host is degraded."
    
    response = make_response(message.format(
            socket.gethostbyname(socket.gethostname()), percentage, threshold))
    
    if not threshold_met:
        response.headers['x-envoy-degraded'] = '*'
    
    return response

@app.route('/trace/<service_number>')
def trace(service_number):
    headers = {}
    # call service 2 from service 1
    if int(os.environ['SERVICE_NAME']) == 1:
        for header in TRACE_HEADERS_TO_PROPAGATE:
            if header in request.headers:
                headers[header] = request.headers[header]
        requests.get("http://localhost:9000/trace/2", headers=headers)
    return (
        'Hello from behind Envoy (service {})! hostname: {} resolved'
        'hostname: {}\n'.format(
            os.environ['SERVICE_NAME'], socket.gethostname(),
            socket.gethostbyname(socket.gethostname())))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
