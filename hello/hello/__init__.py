from time import sleep
from random import lognormvariate

from flask import Flask, Response, jsonify, request
from prometheus_client import (
    Counter, Histogram, Info, make_wsgi_app
)
from werkzeug.wsgi import DispatcherMiddleware


__version__ = '1.0.0'


def create_app():

    app = Flask(__name__)

    app.request_counter = Counter(
        'hello_request_count', 'Request throughput', ('name', )
    )

    app.request_latency = Histogram(
        'hello_latency_seconds', 'Request latency')

    app.version = Info(
        'hello_version', 'Hello version'
    ).info({'version': __version__})

    @app.route('/')
    @app.route('/<name>')
    @app.request_latency.time()
    def hello(name='Stranger'):
        app.request_counter.labels(name=name, pid=PID).inc()
        sleep(lognormvariate(1, 1/8))
        return jsonify(f'Hello {name}!')

    return app


application = DispatcherMiddleware(
    create_app(), {
        '/metrics': make_wsgi_app()
    }
)