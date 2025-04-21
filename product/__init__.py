import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS

from .config.db import create_db, get_uri_db

def create_app() -> Flask:
    _app = Flask(__name__, instance_relative_config=True)
    _app.config['TESTING'] = os.getenv('APP_ENV', 'prod') == 'testing'
    _app.config['PROPAGATE_EXCEPTIONS'] = True
    _app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    _app.config['SQLALCHEMY_DATABASE_URI'] = get_uri_db()

    app_context = _app.app_context()
    app_context.push()

    CORS(_app, origins='*')

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

    create_db(_app)

    from .api import products
    _app.register_blueprint(products.bp)

    @_app.route('/products/health')
    def health():
        return jsonify({'status': 'up'})

    return _app