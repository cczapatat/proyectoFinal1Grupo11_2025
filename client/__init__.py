import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS

from .config.db import create_db, get_uri_db


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config['TESTING'] = os.getenv('APP_ENV', 'prod') == 'testing'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = get_uri_db()

    app_context = app.app_context()
    app_context.push()

    CORS(app, origins='*')

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

    create_db(app)

    from .api import clients
    app.register_blueprint(clients.bp)

    @app.route('/clients/health')
    def health():
        return jsonify({'status': 'up'})

    return app
