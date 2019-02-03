from flask import Flask, jsonify


def create_app():

    app = Flask(__name__)

    @app.route('/')
    @app.route('/<name>')
    def hello(name='Stranger'):
        return jsonify(f'Hello {name}!')

    return app

