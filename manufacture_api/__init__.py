import logging
from flask import Flask, jsonify
from flask_cors import CORS

from .config.db import create_db, get_uri_db
from .blueprints.bulk_task_blueprint import bulk_task_blueprint
from .blueprints.manufacturer_blueprint import manufacturer_blueprint
from .errors.errors import ApiError
import os

def get_env_variable(var_name, default_value):
    return os.environ.get(var_name, default_value)


def create_app( )-> Flask:
    _app = Flask(__name__, instance_relative_config=True)
    _app.config['TESTING'] = os.getenv('APP_ENV', 'prod') == 'testing'
    _app.config['PROPAGATE_EXCEPTIONS'] = True
    _app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    _app.config['SQLALCHEMY_DATABASE_URI'] = get_uri_db()

    app_context = _app.app_context()
    app_context.push()

    CORS(_app, origins="*")

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

    create_db(_app)

    _app.register_blueprint(bulk_task_blueprint)
    _app.register_blueprint(manufacturer_blueprint)

    @_app.errorhandler(ApiError)
    def handle_exception(err):
        response = {"msg": err.description}
        return jsonify(response), err.code
    
    return _app

