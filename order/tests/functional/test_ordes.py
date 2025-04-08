import json
import os
import uuid
import requests_mock
from unittest.mock import patch

user_session_manager_path = os.getenv('USER_SESSION_MANAGER_PATH', default='http://localhost:3008')
sellers_path = os.getenv('SELLERS_PATH', default='http://localhost:3007')
clients_path = os.getenv('CLIENTS_PATH', default='http://localhost:3009')
stocks_api_path = os.getenv('STOCKS_API_PATH', default='http://localhost:3010')

client_id = str(uuid.uuid4())
seller_id = str(uuid.uuid4())
product_one_id = str(uuid.uuid4())
product_two_id = str(uuid.uuid4())

order_data_mock = {
    "client_id": client_id,
    "delivery_date": "2024-06-09 23:59:30",
    "payment_method": "CREDIT_CARD",
    "products": [
        {
            "product_id": product_one_id,
            "units": 25
        },
        {
            "product_id": product_two_id,
            "units": 15
        }
    ],
}


def test_unauthorized_access(client):
    response = client.post('/orders/create', headers={'Content-Type': 'application/json'}, json=order_data_mock)
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'x-token required'


def test_invalid_token(client):
    headers = {
        'x-token': 'invalid_token',
        'Content-Type': 'application/json'
    }

    response = client.post('/orders/create', headers=headers, json=order_data_mock)
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'x-token required'


def test_create_order_missing_auth(client, headers):
    response = client.post('/orders/create', headers=headers, json=order_data_mock)
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'authorization required'


def test_create_order_invalid_auth(client, headers):
    headers['Authorization'] = 'Bearer invalid_token'
    with requests_mock.Mocker() as m:
        m.get(f'{user_session_manager_path}/user_sessions/auth', status_code=401)
        response = client.post('/orders/create', headers=headers, json=order_data_mock)
        data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'authorization required'


def test_create_order_invalid_auth_error(client, headers):
    headers['Authorization'] = 'Bearer invalid_token'
    with requests_mock.Mocker() as m:
        m.get(f'{user_session_manager_path}/user_sessions/auth', status_code=404)
        response = client.post('/orders/create', headers=headers, json=order_data_mock)
        data = json.loads(response.data)

    assert response.status_code == 500
    assert data['message'] == 'internal server error on user_session_manager'


def test_create_order_seller_required_because_auth_is_admin(client, headers):
    headers['Authorization'] = 'Bearer valid_token'
    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': str(uuid.uuid4()),
            'user_type': 'ADMIN'
        })
        # Mock seller not found
        m.get(f'{sellers_path}/sellers/by-id/{seller_id}', status_code=404)

        response = client.post('/orders/create', headers=headers, json=order_data_mock)
        data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'seller_id is required'


def test_create_order_seller_not_found(client, headers):
    headers['Authorization'] = 'Bearer valid_token'
    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': str(uuid.uuid4()),
            'user_type': 'ADMIN'
        })
        # Mock seller not found
        m.get(f'{sellers_path}/sellers/by-id/{seller_id}', status_code=404)

        order_data_mock_in = order_data_mock.copy()
        order_data_mock_in['seller_id'] = seller_id
        response = client.post('/orders/create', headers=headers, json=order_data_mock_in)
        data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'seller not found'


def test_create_order_client_not_found(client, headers):
    headers['Authorization'] = 'Bearer valid_token'
    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': str(uuid.uuid4()),
            'user_type': 'ADMIN'
        })
        # Mock seller found
        m.get(f'{sellers_path}/sellers/by-id/{seller_id}', json={'id': seller_id})
        # Mock client not found
        m.get(f'{clients_path}/clients/client-id/{client_id}/seller-id/{seller_id}', status_code=404)

        order_data_mock_in = order_data_mock.copy()
        order_data_mock_in['seller_id'] = seller_id
        response = client.post('/orders/create', headers=headers, json=order_data_mock_in)
        data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'client not found'


def test_create_order_client_when_auth_is_seller(client, headers):
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

        response = client.post('/orders/create', headers=headers, json=order_data_mock)
        data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'client not found'


def test_create_order_products_http_not_found(client, headers):
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
        # Mock products not found
        m.post(f'{stocks_api_path}/stocks-api/stocks/by-ids', json=[], status_code=404)

        response = client.post('/orders/create', headers=headers, json=order_data_mock)
        data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'product stocks not found'


def test_create_order_products_not_found(client, headers):
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
        # Mock products not found
        m.post(f'{stocks_api_path}/stocks-api/stocks/by-ids', json=[])

        response = client.post('/orders/create', headers=headers, json=order_data_mock)
        data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'product stocks not found'


def test_create_order_products_not_enough_not_found(client, headers):
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
        # Mock products not found
        m.post(f'{stocks_api_path}/stocks-api/stocks/by-ids', json=[
            {'id': str(uuid.uuid4()), 'quantity_in_stock': 10},
            {'id': str(uuid.uuid4()), 'quantity_in_stock': 10},
        ])

        response = client.post('/orders/create', headers=headers, json=order_data_mock)
        data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == f'not enough product stocks {order_data_mock["products"][0]["product_id"]}'


def test_create_order_products_not_enough_quantity_in_stock(client, headers):
    headers['Authorization'] = 'Bearer valid_token'
    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': str(uuid.uuid4()),
            'user_type': 'ADMIN'
        })
        # Mock seller found
        m.get(f'{sellers_path}/sellers/by-id/{seller_id}', json={'id': seller_id})
        # Mock client found
        m.get(f'{clients_path}/clients/client-id/{client_id}/seller-id/{seller_id}',
              json={'id': client_id})
        # Mock products found with stock
        m.post(f'{stocks_api_path}/stocks-api/stocks/by-ids', json=[
            {'id': product_one_id, 'quantity_in_stock': 5},
            {'id': product_two_id, 'quantity_in_stock': 5}
        ])

        order_data_mock_in = order_data_mock.copy()
        order_data_mock_in['seller_id'] = seller_id
        response = client.post('/orders/create', headers=headers, json=order_data_mock_in)
        data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == f'not enough product stocks {order_data_mock["products"][0]["product_id"]}'


def test_create_order_success(client, headers, mock_pubsub):
    headers['Authorization'] = 'Bearer valid_token'
    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': str(uuid.uuid4()),
            'user_type': 'ADMIN'
        })
        # Mock seller found
        m.get(f'{sellers_path}/sellers/by-id/{seller_id}', json={'id': seller_id})
        # Mock client found
        m.get(f'{clients_path}/clients/client-id/{client_id}/seller-id/{seller_id}',
              json={'id': client_id})
        # Mock products found with stock
        m.post(f'{stocks_api_path}/stocks-api/stocks/by-ids', json=[
            {'id': product_one_id, 'quantity_in_stock': 100},
            {'id': product_two_id, 'quantity_in_stock': 50}
        ])

        order_data_mock_in = order_data_mock.copy()
        order_data_mock_in['seller_id'] = seller_id
        response = client.post('/orders/create', headers=headers, json=order_data_mock_in)
        data = json.loads(response.data)

    assert response.status_code == 201
    assert 'id' in data
    assert data['client_id'] == client_id
    assert data['seller_id'] == seller_id
    assert len(data['products']) == 2
    assert mock_pubsub.publish.called


def test_create_order_error_bd_integrity(client, headers):
    headers['Authorization'] = 'Bearer valid_token'
    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': str(uuid.uuid4()),
            'user_type': 'ADMIN'
        })
        # Mock seller found
        m.get(f'{sellers_path}/sellers/by-id/{seller_id}', json={'id': seller_id})
        # Mock client found
        m.get(f'{clients_path}/clients/client-id/{client_id}/seller-id/{seller_id}',
              json={'id': client_id})
        # Mock products found with stock
        m.post(f'{stocks_api_path}/stocks-api/stocks/by-ids', json=[
            {'id': product_one_id, 'quantity_in_stock': 99999999999999999999999999999999999},
            {'id': product_two_id, 'quantity_in_stock': 99999999999999999999999999999999999}
        ])

        order_data_mock_in = order_data_mock.copy()
        order_data_mock_in['seller_id'] = seller_id
        order_data_mock_in['products'][0]['units'] = 99999999999999999999999999999999999
        response = client.post('/orders/create', headers=headers, json=order_data_mock_in)
        data = json.loads(response.data)

    assert response.status_code == 409
    assert data['message'] == 'Database integrity error. 9h9h'
