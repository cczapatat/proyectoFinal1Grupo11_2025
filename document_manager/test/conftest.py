from unittest.mock import Mock
import os

import pytest

from document_manager import create_app


@pytest.fixture
def app():
    os.environ['TESTING'] = 'true'
    app = create_app()
    app.config['TESTING'] = True

    yield app
    from document_manager.config.db import db
    db.session.rollback()
    db.session.close()
    db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def mock_storage(monkeypatch):
    """Mock Cloud Storage client for all tests"""
    # Set testing environment variable first
    os.environ['TESTING'] = 'true'

    mock_blob = Mock()
    mock_blob.upload_from_file.return_value = None

    def mock_download_to_file(buffer):
        buffer.write(b"name,age\nJohn,30\nDoe,25")

    mock_blob.download_to_file.side_effect = mock_download_to_file

    mock_blob.name = 'test_blob'
    mock_blob.content_type = 'text/csv'

    mock_bucket = Mock()
    mock_bucket.blob.return_value = mock_blob

    mock_storage_client = Mock()
    mock_storage_client.bucket.return_value = mock_bucket

    # Mock the storage client
    monkeypatch.setattr('google.cloud.storage.Client', Mock(return_value=mock_storage_client))

    return mock_storage_client
