import logging
import os
import threading

from flask import Flask, jsonify
from flask_cors import CORS

from .config.db import create_db, get_uri_db
from .consumer.stock_update import stock_update_consume_messages


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

    from .api import alarms
    app.register_blueprint(alarms.bp)

    @app.route('/monitor/health')
    def health():
        return jsonify({'status': 'up'})

    thread = threading.Thread(target=stock_update_consume_messages, args=(app,), daemon=True)
    thread.start()

    return app
