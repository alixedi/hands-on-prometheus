from flask import Flask, jsonify


def create_app():

    app = Flask(__name__)

    app.request_counter = Counter(
        'hello_request_count',
        'Request throughput',
        ('name', )
    )

    @app.route('/')
    @app.route('/<name>')
    def hello(name='Stranger'):
        app.request_counter.labels(name=name).inc()
        return jsonify(f'Hello {name}!')

    return app

