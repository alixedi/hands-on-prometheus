import os
from time import sleep
from random import random

from flask import Flask, jsonify, request
from prometheus_client import Histogram, make_wsgi_app
from werkzeug.wsgi import DispatcherMiddleware


def create_app():

    app = Flask(__name__)

    app.payment_latency = Histogram(
        'payment_latency_seconds',
        'Payment processing latency',
        buckets=[x / 10 for x in range(10)]
    )

    @app.payment_latency.time()
    def process_payment(payment_info):
        """Simulate latency of payment processing
        """
        delay_in_sec = random()
        sleep(delay_in_sec)

    @app.route('/checkout', methods=('POST', ))
    def checkout():
        payment_info = request.get_json()
        process_payment(payment_info)
        return jsonify('Thank you!'), 200

    return app


application = DispatcherMiddleware(
    create_app(), {
        '/metrics': make_wsgi_app()
    }
)