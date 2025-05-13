import os
from unittest.mock import Mock, MagicMock

import pytest

from monitor import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    os.environ['TESTING'] = 'true'
    os.environ['FIREBASE_PATH'] = os.path.join(os.path.dirname(__file__), 'src_mocks/firebase-cred.json')
    os.environ['FIREBASE_DATABASE_MISO'] = 'https://any-project-2025.firebaseio.com/'

    yield app
    from monitor.config.db import db
    db.session.rollback()
    db.session.close()
    db.drop_all()

    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def headers():
    return {
        'x-token': os.getenv('INTERNAL_TOKEN', default='internal_token'),
        'Content-Type': 'application/json',
    }


@pytest.fixture(autouse=True)
def mock_pubsub(monkeypatch):
    """Mock PubSub client for all tests"""
    mock_subscriber = Mock()
    mock_subscriber.subscribe.return_value = MagicMock()
    mock_subscriber.subscription_path.return_value = 'mock_topic_path'

    def mock_client():
        return mock_subscriber

    monkeypatch.setattr('google.cloud.pubsub_v1.SubscriberClient', mock_client)
    return mock_subscriber


@pytest.fixture(autouse=True)
def mock_firebase(monkeypatch):
    """Mock Firebase client for all tests"""
    mock_initialize_app = Mock(return_value=None)
    mock_certificate = Mock()
    mock_reference = Mock()

    monkeypatch.setattr('firebase_admin.initialize_app', mock_initialize_app)
    monkeypatch.setattr('firebase_admin.credentials.Certificate', mock_certificate)
    monkeypatch.setattr('firebase_admin.db.reference', mock_reference)

    return {
        'initialize_app': mock_initialize_app,
        'Certificate': mock_certificate,
        'reference': mock_reference,
    }

