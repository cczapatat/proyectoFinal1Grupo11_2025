import os
import requests_mock

from user_session_manager.models.user_session_model import UserSession

host_seller = os.environ.get('SELLERS_PATH', 'http://localhost:3007')
host_client = os.environ.get('CLIENTS_PATH', 'http://localhost:3009')


def test_create_user_session_seller(client, headers):
    with requests_mock.Mocker() as m:
        m.post(f'{host_seller}/sellers/create', json={
            'id': '123',
            'name': 'Test Seller',
            'email': 'seller@test.com'
        }, status_code=201)

        response = client.post('/user_sessions/create',
                               headers=headers,
                               json={
                                   'email': 'seller@test.com',
                                   'password': 'password123',
                                   'type': 'SELLER'
                               }
                               )

        assert response.status_code == 201
        assert 'token' in response.json
        assert response.json['email'] == 'seller@test.com'


def test_create_user_session_client(client, headers):
    with requests_mock.Mocker() as m:
        m.post(f'{host_client}/clients/create', json={
            'id': '456',
            'name': 'Test Client',
            'email': 'client@test.com'
        }, status_code=201)

        response = client.post('/user_sessions/create',
                               headers=headers,
                               json={
                                   'email': 'client@test.com',
                                   'password': 'password123',
                                   'type': 'CLIENT'
                               }
                               )

        assert response.status_code == 201
        assert 'token' in response.json
        assert response.json['email'] == 'client@test.com'


def test_login_success(client, headers):
    with requests_mock.Mocker() as m:
        m.post(f'{host_seller}/sellers/create', json={
            'id': '123',
            'email': 'seller@test.com'
        }, status_code=201)

        client.post('/user_sessions/create',
                    headers=headers,
                    json={
                        'email': 'seller@test.com',
                        'password': 'password123',
                        'type': 'SELLER'
                    }
                    )
        user_session = UserSession.query.filter_by(email='seller@test.com').first()
        m.get(f'{host_seller}/sellers/{user_session.id}', json={
            'id': '123',
            'email': 'seller@test.com'
        }, status_code=200)

        response = client.post('/user_sessions/login',
                               headers=headers,
                               json={
                                   'email': 'seller@test.com',
                                   'password': 'password123'
                               }
                               )

        assert response.status_code == 200
        assert 'token' in response.json


def test_login_success_client(client, headers):
    with requests_mock.Mocker() as m:
        # Create client user session first
        m.post(f'{host_client}/clients/create', json={
            'id': '456',
            'email': 'client@test.com'
        }, status_code=201)

        client.post('/user_sessions/create',
                    headers=headers,
                    json={
                        'email': 'client@test.com',
                        'password': 'password123',
                        'type': 'CLIENT'
                    }
                    )

        user_session = UserSession.query.filter_by(email='client@test.com').first()

        # Mock get client endpoint
        m.get(f'{host_client}/clients/{user_session.id}', json={
            'id': '456',
            'email': 'client@test.com'
        }, status_code=200)

        response = client.post('/user_sessions/login',
                               headers=headers,
                               json={
                                   'email': 'client@test.com',
                                   'password': 'password123'
                               }
                               )

        assert response.status_code == 200
        assert 'token' in response.json
        assert response.json['type'] == 'CLIENT'


def test_login_failed_client_not_found(client, headers):
    with requests_mock.Mocker() as m:
        # Create client user session
        m.post(f'{host_client}/clients/create', json={
            'id': '456',
            'email': 'client@test.com'
        }, status_code=201)

        client.post('/user_sessions/create',
                    headers=headers,
                    json={
                        'email': 'client@test.com',
                        'password': 'password123',
                        'type': 'CLIENT'
                    }
                    )

        user_session = UserSession.query.filter_by(email='client@test.com').first()

        # Mock get client endpoint to return 404
        m.get(f'{host_client}/clients/{user_session.id}', status_code=404)

        response = client.post('/user_sessions/login',
                               headers=headers,
                               json={
                                   'email': 'client@test.com',
                                   'password': 'password123'
                               }
                               )

        assert response.status_code == 401
        assert response.json['message'] == 'invalid credentials'


def test_validate_token(client, headers):
    with requests_mock.Mocker() as m:
        m.post(f'{host_seller}/sellers/create', json={
            'id': '123',
            'email': 'seller@test.com'
        }, status_code=201)

        response = client.post('/user_sessions/create',
                               headers=headers,
                               json={
                                   'email': 'seller@test.com',
                                   'password': 'password123',
                                   'type': 'SELLER'
                               }
                               )

        assert 'token' in response.json

        token = response.json['token']
        headers['Authorization'] = f'Bearer {token}'

        response = client.get('/user_sessions/auth', headers=headers)

        assert response.status_code == 200
        assert 'user_session_id' in response.json
        assert 'user_type' in response.json


def test_validate_token_client(client, headers):
    with requests_mock.Mocker() as m:
        m.post(f'{host_client}/clients/create', json={
            'id': '456',
            'email': 'client@test.com'
        }, status_code=201)

        response = client.post('/user_sessions/create',
                               headers=headers,
                               json={
                                   'email': 'client@test.com',
                                   'password': 'password123',
                                   'type': 'CLIENT'
                               }
                               )

        assert 'token' in response.json

        token = response.json['token']
        headers['Authorization'] = f'Bearer {token}'

        response = client.get('/user_sessions/auth', headers=headers)

        assert response.status_code == 200
        assert 'user_session_id' in response.json
        assert 'user_type' in response.json
        assert response.json['user_type'] == 'CLIENT'
