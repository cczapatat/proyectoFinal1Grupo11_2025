import pytest
import requests_mock
import os
from unittest.mock import Mock

from dotenv import load_dotenv, find_dotenv
from manufacture_api.commands.create_command import CreateBulkTask
from manufacture_api.commands.create_manufacturer import CreateManufacturer
from manufacture_api.commands.get_all_manufacturer import GetAllManufacturer
from manufacture_api.commands.reset import ResetBulkTask
from manufacture_api import create_app

@pytest.fixture
def app():
    os.environ['TESTING'] = 'True'
    app = create_app()
    app.config['TESTING'] = True

    yield app
    from manufacture_api.config.db import db
    db.session.rollback()
    db.session.close()
    db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_api():
    with requests_mock.Mocker() as m:
        yield m

@pytest.fixture
def create_bulk_task(mock_api):
  create_bulk_task = CreateBulkTask()
  return create_bulk_task

@pytest.fixture
def create_manufacturer(mock_api):
  create_manufacturer = CreateManufacturer()
  return create_manufacturer

@pytest.fixture
def get_all_manufacturer(mock_api):
  get_all_manufacturer = GetAllManufacturer()
  return get_all_manufacturer

@pytest.fixture
def reset_bulk_task(mock_api):
  reset_bulk_task = ResetBulkTask()
  return reset_bulk_task

def pytest_configure(config):
  env_file = find_dotenv('../.env.test')
  load_dotenv(env_file)
  return config

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