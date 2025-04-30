import os

from flask import Flask, jsonify
from flask_cors import CORS


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config['TESTING'] = os.getenv('APP_ENV', 'prod') == 'testing'
    app.config['PROPAGATE_EXCEPTIONS'] = True

    app_context = app.app_context()
    app_context.push()

    CORS(app, origins='*')

    from .api import routes
    app.register_blueprint(routes.bp)

    @app.route('/routes/health')
    def health():
        return jsonify({'status': 'up'})

    return app
