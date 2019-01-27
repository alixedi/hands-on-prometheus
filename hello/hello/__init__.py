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
        'Number of requests to hello',
        ('name', 'ua_platform', 'ua_browser')
    )

    app.latency = Histogram(
        'hello_latency',
        'Request latency for hello'
    )

    app.version = Info(
        'hello_version',
        'Version of hello app'
    ).info({
        'version': __version__
    })

    app.concurrent = Gauge(
        'hello_concurrent',
        'Requests being served right now',
        multiprocess_mode='livesum'
    )

    def get_request_metrics():
        return {
            'ua_platform': request.user_agent.platform,
            'ua_browser': request.user_agent.browser,
        }

    @app.route('/')
    @app.route('/<name>')
    @app.latency.time()
    @app.concurrent.track_inprogress()
    def hello(name='stranger'):
        sleep(random())
        app.hello_count.labels(
            **get_request_metrics(),
            **{'name': name}
        ).inc()
        return jsonify(
            f'Hello {name}!'
        )

    return app
