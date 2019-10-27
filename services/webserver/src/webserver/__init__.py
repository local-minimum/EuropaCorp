import os

from .api import create_app

from flask import Response, request
from prometheus_client import (
    multiprocess, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST,
    Counter
)


app = create_app()
app.config.update(**os.environ)

REQUEST_COUNTER = Counter(
    'flask_requests_total',
    'Number of requests by method, status and enpoint',
    ['path',  'http_status', 'method']
)


@app.route("/metrics")
def metrics():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    data = generate_latest(registry)
    return Response(data, mimetype=CONTENT_TYPE_LATEST)


@app.after_request
def counting(response):

    REQUEST_COUNTER.labels(
        request.url_rule if request.url_rule else request.url,
        response.status_code, request.method).inc()

    return response
