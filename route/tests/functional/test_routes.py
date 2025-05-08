import json
import os
import uuid

import requests_mock

user_session_manager_path = os.getenv('USER_SESSION_MANAGER_PATH', default='http://localhost:3008')
visits_path = os.getenv('VISITS_PATH', default='http://localhost:3020')

client_id = str(uuid.uuid4())
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
    response = client.post('/routes/visits/create', headers={'Content-Type': 'application/json'}, json=visit_data_mock)
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'x-token required'


def test_invalid_token(client):
    headers = {
        'x-token': 'invalid_token',
        'Content-Type': 'application/json'
    }

    response = client.post('/routes/visits/create', headers=headers, json=visit_data_mock)
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'x-token required'


def test_create_visit_missing_auth(client, headers):
    response = client.post('/routes/visits/create', headers=headers, json=visit_data_mock)
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'authorization required'


def test_create_visit_invalid_auth(client, headers):
    headers['Authorization'] = 'Bearer invalid_token'
    with requests_mock.Mocker() as m:
        m.get(f'{user_session_manager_path}/user_sessions/auth', status_code=401)
        response = client.post('/routes/visits/create', headers=headers, json=visit_data_mock)
        data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'authorization required'


def test_create_visit_invalid_auth_error(client, headers):
    headers['Authorization'] = 'Bearer invalid_token'
    with requests_mock.Mocker() as m:
        m.get(f'{user_session_manager_path}/user_sessions/auth', status_code=404)
        response = client.post('/routes/visits/create', headers=headers, json=visit_data_mock)
        data = json.loads(response.data)

    assert response.status_code == 500
    assert data['message'] == 'internal server error on user_session_manager'


def test_create_visit_seller_required_because_auth_is_admin(client, headers):
    headers['Authorization'] = 'Bearer valid_token'
    with requests_mock.Mocker() as m:
        # Mock auth response
        seller_id = str(uuid.uuid4())
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': seller_id,
            'user_type': 'SELLER',
        })

        # Mock visit creation response
        m.post(f'{visits_path}/visits/create', json={
            'id': str(uuid.uuid4()),
            'client_id': visit_data_mock['client_id'],
            'seller_id': seller_id,
            'visit_date': visit_data_mock['visit_date'],
            'description': visit_data_mock['description'],
            'products': visit_data_mock['products'],
        }, status_code=201)

        response = client.post('/routes/visits/create', headers=headers, json=visit_data_mock)
        data = json.loads(response.data)

    assert response.status_code == 201
    assert 'id' in data
    assert data['client_id'] == visit_data_mock['client_id']
    assert data['visit_date'] == visit_data_mock['visit_date']
    assert data['description'] == visit_data_mock['description']
    assert data['products'] == visit_data_mock['products']
    assert data['seller_id'] == seller_id


def test_get_all_visits_by_visit_date_missing_date(client, headers):
    headers['Authorization'] = 'Bearer valid_token'
    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': str(uuid.uuid4()),
            'user_type': 'SELLER',
        })

        response = client.get('/routes/visits/get_by_visit_date', headers=headers)
        data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'visit_date required'


def test_get_all_visits_by_visit_date_unauthorized(client):
    response = client.get('/routes/visits/get_by_visit_date', headers={'Content-Type': 'application/json'})
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'x-token required'


def test_get_all_visits_by_visit_date_success(client, headers):
    headers['Authorization'] = 'Bearer valid_token'
    visit_date = '2024-06-09'
    visits_mock = [
        {
            'id': str(uuid.uuid4()),
            'client_id': client_id,
            'visit_date': visit_date,
            'description': 'Visit description',
            'products': visit_data_mock['products'],
        }
    ]

    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': str(uuid.uuid4()),
            'user_type': 'SELLER',
        })

        # Mock get visits response
        m.get(f'{visits_path}/visits/by-visit-date/{visit_date}', json=visits_mock, status_code=200)

        response = client.get(f'/routes/visits/get_by_visit_date?visit_date={visit_date}', headers=headers)
        data = json.loads(response.data)

    assert response.status_code == 200
    assert data == visits_mock
