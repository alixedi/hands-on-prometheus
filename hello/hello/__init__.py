from flask import (
    Flask, 
    Response, 
    jsonify,
    current_app as app
)
from werkzeug.wsgi import DispatcherMiddleware
from prometheus_client import (
    make_wsgi_app,
    Counter,
    generate_latest,
    CONTENT_TYPE_LATEST
)


def create_app():

    app = Flask(__name__)
    app.hello_count = Counter(
        'hello_count',
        'Number of requests to /'
    )

    @app.route('/')
    @app.route('/<name>')
    def hello(name='stranger'):
        app.hello_count.inc()
        return jsonify(
            f'Hello {name}!'
        )

    return app


application = DispatcherMiddleware(
    create_app(), {
        '/metrics': make_wsgi_app()
    }
)