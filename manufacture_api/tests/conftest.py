import pytest
import requests_mock
from dotenv import load_dotenv, find_dotenv
from src.commands.create_command import CreateBulkTask
from src.commands.create_manufacturer import CreateManufacturer
from src.commands.filter_command import FilterBulkTaskByUserEmail, FilterBulkTaskById
from src.commands.get_all_manufacturer import GetAllManufacturer
from src.commands.reset import ResetBulkTask
from src.commands.update_command import BulkTaskUpdate

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
def filter_bulk_task_by_user_email(mock_api):
  filter_bulk_task_by_user_email = FilterBulkTaskByUserEmail()
  return filter_bulk_task_by_user_email

@pytest.fixture
def filter_bulk_task_by_id(mock_api):
  filter_bulk_task_by_id = FilterBulkTaskById()
  return filter_bulk_task_by_id

@pytest.fixture
def get_all_manufacturer(mock_api):
  get_all_manufacturer = GetAllManufacturer()
  return get_all_manufacturer

@pytest.fixture
def reset_bulk_task(mock_api):
  reset_bulk_task = ResetBulkTask()
  return reset_bulk_task

@pytest.fixture
def bulk_task_update(mock_api):
  bulk_task_update = BulkTaskUpdate()
  return bulk_task_update

def pytest_configure(config):
  env_file = find_dotenv('../.env.test')
  load_dotenv(env_file)
  return config