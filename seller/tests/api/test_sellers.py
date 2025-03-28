import json
import uuid
import random
from flask import jsonify
import pytest

def generate_valid_phone():
    length = random.randint(10, 14)  # Minimum 10 digits, up to 14
    first_digit = random.randint(1, 9)  # 1-9
    rest_digits = ''.join([str(random.randint(0, 9)) for _ in range(length - 1)])
    return f"+{first_digit}{rest_digits}"


def test_create_seller_duplicate_email(client, headers, faker):
    # Generate a common email for both requests
    common_email = faker.email()
    seller_data = {
        "user_id": str(uuid.uuid4()),
        "name": faker.name(),
        "phone": generate_valid_phone(),
        "email": common_email,
        "zone": "NORTH",
        "quota_expected": 1000.0,
        "currency_quota": "USD",
        "quartely_target": 2000.0,
        "currency_target": "USD",
        "performance_recomendations": faker.text(max_nb_chars=250)
    }
    # First creation should succeed
    response = client.post('/sellers/create', json=seller_data, headers=headers)
    assert response.status_code == 201

    # Second creation with same email should fail
    seller_data['user_id'] = str(uuid.uuid4())  # New user_id
    seller_data['phone'] = generate_valid_phone()  # New phone
    response = client.post('/sellers/create', json=seller_data, headers=headers)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'message' in data

def test_get_seller_by_id_success(client, headers, faker):
    # First create a seller
    user_id = str(uuid.uuid4())
    seller_data = {
        "user_id": user_id,
        "name": faker.name(),
        "phone": generate_valid_phone(),
        "email": faker.email(),
        "zone": "NORTH",
        "quota_expected": 1000.0,
        "currency_quota": "USD",
        "quartely_target": 2000.0,
        "currency_target": "USD",
        "performance_recomendations": faker.text(max_nb_chars=250)
    }
    response = client.post('/sellers/create', json=seller_data, headers=headers)
    assert response.status_code == 201
    created_seller = json.loads(response.data)

    # Then get the seller by ID
    response = client.get(f'/sellers/{user_id}', headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['email'] == seller_data['email']

def test_get_seller_invalid_id(client, headers):
    response = client.get('/sellers/invalid-uuid', headers=headers)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'message' in data

def test_get_seller_not_found(client, headers):
    random_uuid = str(uuid.uuid4())
    response = client.get(f'/sellers/{random_uuid}', headers=headers)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['message'] == 'seller not found'

def test_unauthorized_access(client, faker):
    response = client.get('/sellers/123', headers={'Content-Type': 'application/json'})
    assert response.status_code == 401
    assert b'authorization required' in response.data

def test_invalid_token(client, faker):
    headers = {
        'x-token': 'invalid_token',
        'Content-Type': 'application/json'
    }
    response = client.get('/sellers/123', headers=headers)
    assert response.status_code == 401
    assert b'authorization required' in response.data
