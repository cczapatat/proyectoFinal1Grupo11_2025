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



def test_get_clients_by_seller(client, headers):
    with requests_mock.Mocker() as m:
        m.get(f'{host_client}/clients/seller/17d371c3-74be-47d6-ac25-4b469d693688', json=[
            {
                "address": "AV 123",
                "client_type": "CORNER_STORE",
                "created_at": "Mon, 07 Apr 2025 23:23:18 GMT",
                "email": "pedro20@sta.com",
                "id": "cdfe2684-9683-4056-86d4-9e393c5d9c3a",
                "name": "Pedro Herrera",
                "phone": "+573017084720",
                "updated_at": "Mon, 07 Apr 2025 23:23:18 GMT",
                "user_id": "e3182826-cb26-43ab-a017-4a8bf8f5bbfb",
                "zone": "CENTER"
            }
        ], status_code=200)

        response = client.get('/user_sessions/clients/seller/17d371c3-74be-47d6-ac25-4b469d693688',
                               headers=headers
                               )
        assert response.status_code == 200
        assert len(response.json) == 1

def test_associate_clients_to_seller(client, headers):
    with requests_mock.Mocker() as m:
        m.post(f'{host_client}/clients/associate_seller', json=[
            {
                "address": "AV 123",
                "client_type": "CORNER_STORE",
                "created_at": "Mon, 07 Apr 2025 23:23:18 GMT",
                "email": "pedro20@sta.com",
                "id": "cdfe2684-9683-4056-86d4-9e393c5d9c3a",
                "name": "Pedro Herrera",
                "phone": "+573017084720",
                "updated_at": "Mon, 07 Apr 2025 23:23:18 GMT",
                "user_id": "e3182826-cb26-43ab-a017-4a8bf8f5bbfb",
                "zone": "CENTER"
            }
        ], status_code=200)

        response = client.post('/user_sessions/clients/associate_seller',
                              headers=headers,
                              json={
                                        'client_id': ['cdfe2684-9683-4056-86d4-9e393c5d9c3a'],
                                        'seller_id': '76687dc4-22bf-4277-a983-659e51b84c41'
                              })
        assert response.status_code == 200
        assert len(response.json) == 1

def test_get_sellers(client, headers):
    with requests_mock.Mocker() as m:
        m.get(f'{host_seller}/sellers?page=1&per_page=10&sort_by=name&sort_order=asc', json={
            "data": [
                {
                    "created_at": "2025-04-09T19:22:16.825716",
                    "currency_quota": "COP",
                    "currency_target": "COP",
                    "email": "camilo1@sta.com",
                    "id": "d22cff4d-88ec-454e-ae34-71a36d2cbc8a",
                    "name": "Camilo 12",
                    "performance_recomendations": "don't be a bad boy",
                    "phone": "+573000000001",
                    "quartely_target": 2000000.0,
                    "quota_expected": 1000000.0,
                    "updated_at": "2025-04-09T19:22:16.825716",
                    "user_id": "255e6d10-7fc6-422e-80f7-d4ebd65333dd",
                    "zone": "CENTER"
                },
                {
                    "created_at": "2025-04-09T19:22:27.335807",
                    "currency_quota": "COP",
                    "currency_target": "COP",
                    "email": "camilo2@sta.com",
                    "id": "fad20767-134b-4423-ae6e-267b99bcb4be",
                    "name": "Camilo 2",
                    "performance_recomendations": "don't be a bad boy",
                    "phone": "+573000000002",
                    "quartely_target": 2000000.0,
                    "quota_expected": 1000000.0,
                    "updated_at": "2025-04-09T19:22:27.335807",
                    "user_id": "aa4d5032-76f8-4dc9-a4c8-84c1c0492eea",
                    "zone": "CENTER"
                },
                {
                    "created_at": "2025-04-09T19:22:36.653063",
                    "currency_quota": "COP",
                    "currency_target": "COP",
                    "email": "camilo3@sta.com",
                    "id": "864756e2-04ed-4e13-b7b2-4b472af2a4eb",
                    "name": "Camilo 3",
                    "performance_recomendations": "don't be a bad boy",
                    "phone": "+573000000003",
                    "quartely_target": 2000000.0,
                    "quota_expected": 1000000.0,
                    "updated_at": "2025-04-09T19:22:36.653063",
                    "user_id": "7daf1bed-f841-4f69-8386-56e6f7552409",
                    "zone": "CENTER"
                },
                {
                    "created_at": "2025-04-09T19:22:45.594342",
                    "currency_quota": "COP",
                    "currency_target": "COP",
                    "email": "camilo4@sta.com",
                    "id": "9194b1ff-52ee-48d4-820d-723838c20a32",
                    "name": "Camilo 4",
                    "performance_recomendations": "don't be a bad boy",
                    "phone": "+573000000004",
                    "quartely_target": 2000000.0,
                    "quota_expected": 1000000.0,
                    "updated_at": "2025-04-09T19:22:45.594342",
                    "user_id": "9285da42-01cc-43c7-a8eb-27a1bbaf773e",
                    "zone": "CENTER"
                }
            ],
            "page": 1,
            "per_page": 10,
            "total": 4,
            "total_pages": 1
        }, status_code=200)

        response = client.get('/user_sessions/sellers',
                               headers=headers
                               )
        assert response.status_code == 200
        assert len(response.json['data']) > 1