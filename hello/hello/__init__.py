import os
from time import time, sleep
from random import lognormvariate

from flask import Flask, Response, jsonify, request
from prometheus_client import Counter, Histogram, Info, make_wsgi_app
from werkzeug.wsgi import DispatcherMiddleware


__version__ = '1.0.0'

PID = os.getpid()


def create_app():

    app = Flask(__name__)

    app.request_counter = Counter(
        'hello_request_count',
        'Request throughput',
        ('name', 'pid')
    )

    app.request_latency = Histogram(
        'hello_latency_seconds',
        'Request latency',
        ('pid', ),
        buckets=[x * 0.5 for x in range(20)]
    )

    app.version = Info(
        'hello_version', 'Hello version'
    ).info({'version': __version__})

    @app.before_request
    def _before_request():
        request._t0 = time()

    @app.after_request
    def _after_request(response):
        dt = time() - request._t0
        app.request_latency.labels(pid=PID).observe(dt)
        return response

    @app.route('/')
    @app.route('/<name>')
    def hello(name='Stranger'):
        app.request_counter.labels(name=name, pid=PID).inc()
        sleep(lognormvariate(1, 1/4))
        return jsonify(f'Hello {name}!')

    return app


application = DispatcherMiddleware(
    create_app(), {
        '/metrics': make_wsgi_app()
    }
)