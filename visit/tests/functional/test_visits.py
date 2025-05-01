import json
import os
import uuid

import requests_mock

user_session_manager_path = os.getenv('USER_SESSION_MANAGER_PATH', default='http://localhost:3008')
sellers_path = os.getenv('SELLERS_PATH', default='http://localhost:3007')
clients_path = os.getenv('CLIENTS_PATH', default='http://localhost:3009')

client_id = str(uuid.uuid4())
seller_id = str(uuid.uuid4())
product_one_id = str(uuid.uuid4())
product_two_id = str(uuid.uuid4())

visit_data_mock = {
    "client_id": client_id,
    "description": "Any description to the visit",
    "visit_date": "2024-06-09 23:59:30",
    "products": [
        {
            "product_id": product_one_id,
        },
        {
            "product_id": product_two_id,
        }
    ],
}


def test_unauthorized_access(client):
    response = client.post('/visits/create', headers={'Content-Type': 'application/json'}, json=visit_data_mock)
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'x-token required'


def test_invalid_token(client):
    headers = {
        'x-token': 'invalid_token',
        'Content-Type': 'application/json'
    }

    response = client.post('/visits/create', headers=headers, json=visit_data_mock)
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'x-token required'


def test_create_visit_missing_auth(client, headers):
    response = client.post('/visits/create', headers=headers, json=visit_data_mock)
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'authorization required'


def test_create_visit_invalid_auth(client, headers):
    headers['Authorization'] = 'Bearer invalid_token'
    with requests_mock.Mocker() as m:
        m.get(f'{user_session_manager_path}/user_sessions/auth', status_code=401)
        response = client.post('/visits/create', headers=headers, json=visit_data_mock)
        data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'authorization required'


def test_create_visit_invalid_auth_error(client, headers):
    headers['Authorization'] = 'Bearer invalid_token'
    with requests_mock.Mocker() as m:
        m.get(f'{user_session_manager_path}/user_sessions/auth', status_code=404)
        response = client.post('/visits/create', headers=headers, json=visit_data_mock)
        data = json.loads(response.data)

    assert response.status_code == 500
    assert data['message'] == 'internal server error on user_session_manager'


def test_create_visit_seller_required_because_auth_is_admin(client, headers):
    headers['Authorization'] = 'Bearer valid_token'
    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': str(uuid.uuid4()),
            'user_type': 'ADMIN'
        })

        response = client.post('/visits/create', headers=headers, json=visit_data_mock)
        data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'un authorization operation'


def test_create_visit_seller_not_found(client, headers):
    headers['Authorization'] = 'Bearer valid_token'
    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': seller_id,
            'user_type': 'SELLER'
        })
        # Mock seller not found
        m.get(f'{sellers_path}/sellers/by-id/{seller_id}', status_code=404)

        response = client.post('/visits/create', headers=headers, json=visit_data_mock)
        data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'seller not found'


def test_create_visit_client_not_found(client, headers):
    headers['Authorization'] = 'Bearer valid_token'
    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': seller_id,
            'user_type': 'SELLER'
        })
        # Mock seller found
        m.get(f'{sellers_path}/sellers/by-id/{seller_id}', json={'id': seller_id})
        # Mock client not found
        m.get(f'{clients_path}/clients/client-id/{client_id}/seller-id/{seller_id}', status_code=404)

        response = client.post('/visits/create', headers=headers, json=visit_data_mock)
        data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'client not found'


def test_create_visit_auth_not_response_user_id(client, headers):
    headers['Authorization'] = 'Bearer valid_token'
    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': None,
            'user_type': 'SELLER'
        })

        response = client.post('/visits/create', headers=headers, json=visit_data_mock)
        data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'seller_id is required'


def test_create_visit_success(client, headers):
    headers['Authorization'] = 'Bearer valid_token'
    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': seller_id,
            'user_type': 'SELLER'
        })
        # Mock seller found
        m.get(f'{sellers_path}/sellers/by-id/{seller_id}', json={'id': seller_id})
        # Mock client found
        m.get(f'{clients_path}/clients/client-id/{client_id}/seller-id/{seller_id}',
              json={'id': client_id})

        response = client.post('/visits/create', headers=headers, json=visit_data_mock)
        data = json.loads(response.data)

    assert response.status_code == 201
    assert 'id' in data
    assert data['client_id'] == client_id
    assert data['seller_id'] == seller_id
    assert len(data['products']) == 2
