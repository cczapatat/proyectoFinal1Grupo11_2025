import os
import logging
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from .config.db import create_db, get_uri_db


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config['TESTING'] = os.getenv('APP_ENV', 'prod') == 'testing'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'frase-secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = get_uri_db()

    app_context = app.app_context()
    app_context.push()

    CORS(app, origins='*')

    jwt = JWTManager(app)

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

    create_db(app)

    from .api import user_sessions
    app.register_blueprint(user_sessions.bp)

    @app.route('/user_sessions/health')
    def health():
        return jsonify({'status': 'up'})

    return app
