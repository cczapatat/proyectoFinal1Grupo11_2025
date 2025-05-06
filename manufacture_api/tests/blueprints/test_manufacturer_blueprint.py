import json
import os
from unittest.mock import patch

import requests_mock
from faker import Faker

from manufacture_api.models.Models import MANUFACTURER_COUNTRY

user_session_manager_path = os.getenv('USER_SESSION_MANAGER_PATH', default='http://localhost:3008')
data_factory = Faker()
token = 'internal_token'


def _generate_manufacturer_payload(**overrides):
    payload = {
        "name": data_factory.name(),
        "address": data_factory.address(),
        "phone": '+5730054367' + str(data_factory.random_int(min=1000, max=9999)),
        "email": data_factory.email(),
        "country": data_factory.random_element(
            [country.value for country in MANUFACTURER_COUNTRY]),
        "tax_conditions": data_factory.word(),
        "legal_conditions": data_factory.word(),
        "rating_quality": data_factory.random_int(min=1, max=5),
    }
    payload.update(overrides)
    return payload


def _post_create_manufacturer(client, payload, token_request=None):
    return client.post(
        '/manufacture-api/manufacturers/create',
        headers={'x-token': token_request or token},
        json=payload
    )


def test_create_manufacturer_fail_unauthorized(client):
    payload = _generate_manufacturer_payload()
    response = _post_create_manufacturer(client, payload, data_factory.word())

    assert response.status_code == 401


def test_create_manufacturer_fail_phone_number(client):
    payload = _generate_manufacturer_payload(phone=data_factory.word())
    response = _post_create_manufacturer(client, payload)

    assert response.status_code == 500


def test_create_manufacturer_fail_email(client):
    payload = _generate_manufacturer_payload(email=data_factory.word())
    response = _post_create_manufacturer(client, payload)

    assert response.status_code == 500


def test_create_manufacturer_fail_rating(client):
    payload = _generate_manufacturer_payload(rating_quality=-20)
    response = _post_create_manufacturer(client, payload)

    assert response.status_code == 500


def test_create_manufacturer_fail_country(client):
    payload = _generate_manufacturer_payload(country=data_factory.word())
    response = _post_create_manufacturer(client, payload)

    assert response.status_code == 500


def test_create_manufacturer_success(client):
    payload = _generate_manufacturer_payload()
    response = _post_create_manufacturer(client, payload)

    assert response.status_code == 201
    assert response.json['id'] is not None
    assert response.json['name'] == payload['name']


def test_get_all_manufacturer_success(client):
    response = client.get(
        '/manufacture-api/manufacturers/all',
        headers={'x-token': token}
    )
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_create_massive_manufacturer_without_authorization(client):
    fake_file_id = data_factory.uuid4()
    response = client.post(
        '/manufacture-api/manufacturers/massive/create',
        data=json.dumps({'file_id': fake_file_id}),
        headers={
            'content-type': 'application/json',
            'x-token': 'internal_token'
        }
    )

    assert response.status_code == 401


def test_create_massive_manufacturer_auth_response_unauthorized(client):
    fake_authorization = data_factory.uuid4()
    fake_file_id = data_factory.uuid4()

    with requests_mock.Mocker() as m:
        m.get(
            f'{user_session_manager_path}/user_sessions/auth',
            status_code=401
        )

        response = client.post(
            '/manufacture-api/manufacturers/massive/create',
            data=json.dumps({'file_id': fake_file_id}),
            headers={
                'content-type': 'application/json',
                'x-token': token,
                'Authorization': fake_authorization
            }
        )

    assert response.status_code == 401


def test_create_massive_manufacturer_auth_response_internal_error(client):
    fake_authorization = data_factory.uuid4()
    fake_file_id = data_factory.uuid4()

    with requests_mock.Mocker() as m:
        m.get(
            f'{user_session_manager_path}/user_sessions/auth',
            status_code=500
        )

        response = client.post(
            '/manufacture-api/manufacturers/massive/create',
            data=json.dumps({'file_id': fake_file_id}),
            headers={
                'content-type': 'application/json',
                'x-token': token,
                'Authorization': fake_authorization
            }
        )

    assert response.status_code == 500


def test_create_massive_manufacturer_missing_file_id(client):
    fake_user_id = data_factory.uuid4()
    fake_authorization = data_factory.uuid4()

    with requests_mock.Mocker() as m:
        m.get(
            f'{user_session_manager_path}/user_sessions/auth',
            json={
                'user_session_id': fake_user_id,
                'user_id': fake_user_id,
                'user_type': 'SELLER'
            },
            status_code=200
        )

        response = client.post(
            '/manufacture-api/manufacturers/massive/create',
            data=json.dumps({}),
            headers={
                'content-type': 'application/json',
                'x-token': token,
                'Authorization': fake_authorization
            }
        )

    assert response.status_code == 400
    json_response = json.loads(response.data)
    assert json_response['message'] == 'file_id is required'


@patch('manufacture_api.commands.create_massive_manufacturer.PublisherService.publish_create_command')
def test_create_massive_manufacturer_success_by_seller(mock_pubsub, client):
    fake_user_id = data_factory.uuid4()
    fake_authorization = data_factory.uuid4()
    fake_file_id = data_factory.uuid4()

    mock_pubsub.return_value = True

    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': fake_user_id,
            'user_id': fake_user_id,
            'user_type': 'SELLER'
        })

        response = client.post(
            '/manufacture-api/manufacturers/massive/create',
            data=json.dumps({'file_id': fake_file_id}),
            headers={
                'content-type': 'application/json',
                'x-token': token,
                'Authorization': fake_authorization
            }
        )

    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert json_response['id'] is not None
    mock_pubsub.assert_called_once()


@patch('manufacture_api.commands.create_massive_manufacturer.PublisherService.publish_create_command')
def test_create_massive_manufacturer_success_by_admin(mock_pubsub, client):
    fake_user_id = data_factory.uuid4()
    fake_authorization = data_factory.uuid4()
    fake_file_id = data_factory.uuid4()

    mock_pubsub.return_value = True

    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': fake_user_id,
            'user_id': fake_user_id,
            'user_type': 'ADMIN'
        })

        response = client.post(
            '/manufacture-api/manufacturers/massive/create',
            data=json.dumps({'file_id': fake_file_id}),
            headers={
                'content-type': 'application/json',
                'x-token': token,
                'Authorization': fake_authorization
            }
        )

    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert json_response['id'] is not None
    mock_pubsub.assert_called_once()


def test_create_massive_manufacturer_forbidden_by_other_user_type(client):
    fake_user_id = data_factory.uuid4()
    fake_authorization = data_factory.uuid4()
    fake_file_id = data_factory.uuid4()

    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': fake_user_id,
            'user_id': fake_user_id,
            'user_type': 'OTHER_TYPE_USER'
        })

        response = client.post(
            '/manufacture-api/manufacturers/massive/create',
            data=json.dumps({'file_id': fake_file_id}),
            headers={
                'content-type': 'application/json',
                'x-token': token,
                'Authorization': fake_authorization
            }
        )

    assert response.status_code == 403
    json_response = json.loads(response.data)
    assert json_response['message'] == 'Invalid user type'


@patch('manufacture_api.commands.create_massive_manufacturer.PublisherService.publish_create_command')
def test_create_massive_manufacturer_publish_error(mock_pubsub, client):
    fake_user_id = data_factory.uuid4()
    fake_authorization = data_factory.uuid4()
    fake_file_id = data_factory.uuid4()

    mock_pubsub.return_value = False

    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': fake_user_id,
            'user_id': fake_user_id,
            'user_type': 'SELLER'
        })

        response = client.post(
            '/manufacture-api/manufacturers/massive/create',
            data=json.dumps({'file_id': fake_file_id}),
            headers={
                'content-type': 'application/json',
                'x-token': token,
                'Authorization': fake_authorization
            }
        )

    assert response.status_code == 500
    json_response = json.loads(response.data)
    assert json_response['status'] == 'FAILED'


def test_get_paginate_manufacturer_success(client):
    page = 1
    per_page = 10

    payload_one = _generate_manufacturer_payload()
    response_one = _post_create_manufacturer(client, payload_one)
    assert response_one.status_code == 201

    payload_two = _generate_manufacturer_payload()
    response_two = _post_create_manufacturer(client, payload_two)
    assert response_two.status_code == 201

    response = client.get(
        f'/manufacture-api/manufacturers/list?page={page}&per_page={per_page}',
        headers={'x-token': token}
    )
    response_data = json.loads(response.data)

    assert response.status_code == 200
    assert isinstance(response_data['manufacturers'], list)
    assert len(response_data['manufacturers']) == 2
    assert response_data['total'] == 2
    assert response_data['page'] == page
    assert response_data['per_page'] == per_page
