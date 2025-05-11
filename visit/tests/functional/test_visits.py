import json
import os
import uuid
from datetime import datetime

import pytest
import requests_mock

import sys
from visit.models.visit_model import Visit
from visit.config.db import db

user_session_manager_path = os.getenv('USER_SESSION_MANAGER_PATH', default='http://localhost:3008')
sellers_path = os.getenv('SELLERS_PATH', default='http://localhost:3007')
clients_path = os.getenv('CLIENTS_PATH', default='http://localhost:3009')
visits_path = os.getenv('VISITS_PATH', default='http://localhost:3020')

client_id = str(uuid.uuid4())
seller_id = str(uuid.uuid4())
product_one_id = str(uuid.uuid4())
product_two_id = str(uuid.uuid4())
visit_id = str(uuid.uuid4())

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

visit_client_data_mock = [
    {
        "client": {
            "client_type": "CORNER_STORE",
            "id": client_id,
            "name": "Lucho Herrera",
            "zone": "CENTER"
        },
        "description": "any description test visit",
        "id": visit_id,
        "seller_id": seller_id,
        "visit_date": "2025-10-09 23:59:30"
    }
]


@pytest.fixture
def setup_database():
    # Ensure the database is clean before each test
    db.session.query(Visit).delete()
    db.session.commit()

    # Insert mock data
    visit_date = "2024-06-09"
    visit = Visit(
        id=uuid.uuid4(),
        user_id=str(uuid.uuid4()),
        seller_id=uuid.uuid4(),
        client_id=uuid.uuid4(),
        description="Test visit description",
        visit_date=datetime.strptime(visit_date, '%Y-%m-%d'),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.session.add(visit)
    db.session.commit()

    return visit_date


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

def test_get_all_visits_by_visit_date_paginated_unauthorized(client):
    response = client.get('/visits/by-visit-date-paginated/2024-06-09')
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'x-token required'


def test_get_all_visits_by_visit_date_paginated_invalid_token(client):
    headers = {
        'x-token': 'invalid_token',
    }

    response = client.get('/visits/by-visit-date-paginated/2024-06-09', headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'x-token required'


def test_get_all_visits_by_visit_date_paginated_invalid_date_format(client, headers):
    headers['Authorization'] = 'Bearer valid_token'
    with requests_mock.Mocker() as m:
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': seller_id,
            'user_type': 'SELLER'
        })

        response = client.get('/visits/by-visit-date-paginated/invalid-date', headers=headers)
        data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'Invalid input: time data \'invalid-date\' does not match format \'%Y-%m-%d\''


def test_get_all_visits_by_visit_date_paginated_unauthorized_user_type(client, headers):
    headers['Authorization'] = 'Bearer valid_token'
    with requests_mock.Mocker() as m:
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': seller_id,
            'user_type': 'ADMIN'
        })

        response = client.get('/visits/by-visit-date-paginated/2024-06-09', headers=headers)
        data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'unauthorized operation'


def test_get_all_visits_by_visit_date_paginated_seller_id_missing(client, headers):
    headers['Authorization'] = 'Bearer valid_token'
    with requests_mock.Mocker() as m:
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': None,
            'user_type': 'SELLER'
        })

        response = client.get('/visits/by-visit-date-paginated/2024-06-09', headers=headers)
        data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'seller_id is required'


def test_get_all_visits_by_visit_date_paginated_success(client, headers):
    headers['Authorization'] = 'Bearer valid_token'
    visit_date = '2024-06-09'
    visits_mock = {
        'page': 1,
        'per_page': 10,
        'total': 3,
        'total_pages': 1,
        'data': visit_client_data_mock
    }

    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': str(uuid.uuid4()),
            'user_type': 'SELLER',
        })

        # Mock get visits response
        m.get(f'{visits_path}/visits/by-visit-date-paginated/{visit_date}', json=visits_mock, status_code=200)

        response = client.get(f'/visits/by-visit-date-paginated/{visit_date}?page=1&per_page=5&sort_order=asc', headers=headers)
        data = json.loads(response.data)

    assert response.status_code == 200

