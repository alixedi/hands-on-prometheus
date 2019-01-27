from time import sleep
from random import random

from flask import (
    Flask,
    Response,
    jsonify,
    request,
    current_app as app
)
from prometheus_client import Counter, Histogram, Info, Gauge


__version__ = '1.0.0'


def create_app():

    app = Flask(__name__)

    app.hello_count = Counter(
        'hello_count',
        'Number of requests to /',
        (
            'remote_addr', 'method', 'url', 'name',
            'ua_platform', 'ua_browser', 'ua_version',
            'ua_language'
        )
    )

    app.latency = Histogram(
        'latency',
        'Request latency for endpoints'
    )

    app.version = Info(
        'version',
        'Version of hello app'
    ).info({
        'version': __version__
    })

    app.concurrent = Gauge(
        'concurrent',
        'Requests being served right now'
    )

    def get_request_metrics():
        return {
            'remote_addr': request.remote_addr,
            'method': request.method,
            'url': request.url,
            'ua_platform': request.user_agent.platform,
            'ua_browser': request.user_agent.browser,
            'ua_version': request.user_agent.version,
            'ua_language': request.user_agent.language,
        }

    @app.route('/')
    @app.route('/<name>')
    @app.latency.time()
    @app.concurrent.track_inprogress()
    def hello(name='stranger'):
        sleep(random() * 5)
        app.hello_count.labels(
            **get_request_metrics(),
            **{'name': name}
        ).inc()
        return jsonify(
            f'Hello {name}!'
        )

    return app
