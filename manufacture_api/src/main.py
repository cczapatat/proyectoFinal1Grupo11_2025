import logging
from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from blueprints.bulk_task_blueprint import bulk_task_blueprint
from errors.errors import ApiError
from models.BulkTask import db
import os

def get_env_variable(var_name, default_value):
    return os.environ.get(var_name, default_value)

db_user = get_env_variable('DB_USER', 'postgres')
db_password = get_env_variable('DB_PASSWORD', 'postgres')
db_host = get_env_variable('DB_HOST', 'localhost')
db_port = get_env_variable('DB_PORT', '5432')
db_name = get_env_variable('DB_NAME', 'bulktask')
db_type = get_env_variable('DB_TYPE', 'postgresql')


def create_flask_app():
    _app = Flask(__name__)
    _app.register_blueprint(bulk_task_blueprint)
    _app.config['PROPAGATE_EXCEPTIONS'] = True
    _app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    _app.config['SQLALCHEMY_DATABASE_URI'] = f'{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    CORS(_app, origins="*")

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

    return _app

app = create_flask_app()
db.init_app(app)

with app.app_context():
    db.create_all()

api = Api(app)

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {"msg": err.description}
    return jsonify(response), err.code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(get_env_variable('PORT', 3007)), debug=get_env_variable('DEBUG', 'True').lower() in ['true', '1', 't'])
