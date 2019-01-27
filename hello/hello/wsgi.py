from werkzeug.wsgi import DispatcherMiddleware
from prometheus_client import make_wsgi_app

from hello import create_app


application = DispatcherMiddleware(
    create_app(), {
        '/metrics': make_wsgi_app()
    }
)