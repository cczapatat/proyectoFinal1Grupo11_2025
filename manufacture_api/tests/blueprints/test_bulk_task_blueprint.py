import requests_mock
from faker import Faker
from unittest.mock import MagicMock, Mock, patch

data_factory = Faker()
token = 'internal_token'

def _generate_bulk_task_payload(**overrides):
    payload = {
        "user_id": data_factory.uuid4(),
        "file_id": data_factory.uuid4(),
    }
    payload.update(overrides)
    return payload

def _post_create_bulk_task(client, payload, request_token=None):
    return client.post(
        '/manufacture-api/bulk',
        headers={'x-token': request_token or token},
        json=payload
    )

def _get_bulk_task_by_user_email(client, user_id, request_token=None):
    return client.get(
        f'/manufacture-api/bulk/user?user_id={user_id}',
        headers={'x-token': request_token or token}
    )

def _get_bulk_task_by_user_id(client, id, request_token=None):
    return client.get(
        f'/manufacture-api/bulk/user?user_id={id}',
        headers={'x-token': request_token or token}
    )

def test_create_bulk_task_fail_unauthorized(client):
    payload = _generate_bulk_task_payload()
    response = _post_create_bulk_task(client, payload, data_factory.word())

    assert response.status_code == 401

@patch('manufacture_api.commands.create_command.PublisherService.publish_create_command')
def test_create_bulk_task_success(mock_pubsub, client):
    mock_pubsub.return_value = True

    with requests_mock.Mocker() as m:
        payload = _generate_bulk_task_payload()
        response = _post_create_bulk_task(client, payload)

    assert response.status_code == 201
    assert response.json['id'] is not None
    assert response.json['user_id'] == payload['user_id']