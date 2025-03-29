import os
import pytest
from user_session_manager import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True

    yield app
    from user_session_manager.config.db import db
    db.session.rollback()
    db.session.close()
    db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def headers():
    return {
        'x-token': os.getenv('INTERNAL_TOKEN', default='internal_token'),
        'Content-Type': 'application/json'
    }
