import os
from unittest.mock import Mock

import pytest

from product import create_app


@pytest.fixture
def app():
    os.environ['TESTING'] = 'True'
    app = create_app()
    app.config['TESTING'] = True

    yield app
    from product.config.db import db
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


@pytest.fixture(autouse=True)
def mock_pubsub(monkeypatch):
    """Mock PubSub client for all tests"""
    mock_publisher = Mock()
    mock_publisher.publish.return_value.result.return_value = 'mock_message_id'
    mock_publisher.topic_path.return_value = 'mock_topic_path'

    def mock_client(*args, **kwargs):
        return mock_publisher

    # Mock the PublisherClient globally
    monkeypatch.setattr('google.cloud.pubsub_v1.PublisherClient', mock_client)
    return mock_publisher
