import os
import pytest

from client import create_app


@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config['TESTING'] = True

    yield app
    from client.config.db import db
    db.session.rollback()
    db.session.close()
    db.session.remove()
    db.drop_all()
    db.session.rollback()

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def headers():
    return {
        'x-token': os.getenv('INTERNAL_TOKEN', default='internal_token'),
        'Content-Type': 'application/json'
    }