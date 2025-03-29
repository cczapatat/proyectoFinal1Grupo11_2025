import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = None


def init_db(app: Flask) -> SQLAlchemy:
    global db
    db = SQLAlchemy(app)

    return db


def create_db(app: Flask):
    db_instance = init_db(app)

    with app.app_context():
        from ..models import client_model

        db_instance.create_all()


def get_uri_db() -> str:
    host = os.getenv('DB_HOST', default="127.0.0.1")
    port = os.getenv('DB_PORT', default="5432")
    user = os.getenv('DB_USER', default="user_final")
    password = os.getenv('DB_PASSWORD', default="pass_final")
    db_name = os.getenv('DB_NAME', default="project_final")
    db_type = os.getenv('DB_TYPE', default="postgresql")

    return f'{db_type}://{user}:{password}@{host}:{port}/{db_name}'
