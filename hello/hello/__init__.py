from time import sleep
from random import lognormvariate

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

    # Counter counts events over time. As a result,
    # a Counter can only go up.
    app.hello_count = Counter(
        'hello_count',
        'Number of requests to hello',
        ('name', 'ua_platform', 'ua_browser')
    )

    # Gauge measures rates. As a result, it can go
    # up or down. This implies that we need a strategy
    # to select an appropriate value of the Gauge when
    # our application has multiple processes. We are
    # using `livesum` which sums the Gauges submitted
    # by all live processes.
    app.concurrent = Gauge(
        'hello_concurrent',
        'Requests being served right now'
    )

    # Histogram tracks the size and number of events
    # in buckets. Often useful for request latency.
    app.latency = Histogram(
        'hello_latency',
        'Request latency for hello'
    )

    # Info tracks a key-value pair. Often useful for
    # version strings.
    app.version = Info(
        'hello_version',
        'Version of hello app'
    ).info({
        'version': __version__
    })


    def get_request_metrics():
        """ Parses the request and returns the user-agent
        properties as a dict.
        """
        return {
            'ua_platform': request.user_agent.platform,
            'ua_browser': request.user_agent.browser,
        }

    def arbitrary_delay(mean=1):
        """ This function introduces an arbitrary
        delay with the given maximum when its
        called
        """
        sleep(lognormvariate(mean, mean/4))

    @app.route('/')
    @app.route('/<name>')
    @app.latency.time()
    @app.concurrent.track_inprogress()
    def hello(name='stranger'):
        """ This is the only endpoint in our API.
        GET / returns 'Hello Stranger!'
        GET /<name> returns `Hello <name>!`
        """
        # This is an example of sending application
        # metrics to Prometheus. We want to track
        # the distribution of <name> so we are using
        # it as a label which would add a field or a
        # dimension to the `hello_count` time series
        # in Prometheus.
        # In addition, we are tracking our user's
        # OS (`ua_platform`) and browser (`ua-browser`)
        app.hello_count.labels(
            **get_request_metrics(),
            **{'name': name}
        ).inc()

        # I am putting in a delay here to simulate e.g.
        # database access so that our latency numbers
        # are more interesting
        arbitrary_delay()

        return jsonify(
            f'Hello {name}!'
        )

    return app
