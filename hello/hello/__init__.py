from flask import (
    Flask,
    Response,
    jsonify,
    request,
    current_app as app
)
from prometheus_client import (
    Counter,
    generate_latest,
    CONTENT_TYPE_LATEST
)


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
    def hello(name='stranger'):
        app.hello_count.labels(
            **get_request_metrics(),
            **{'name': name}
        ).inc()
        return jsonify(
            f'Hello {name}!'
        )

    return app
