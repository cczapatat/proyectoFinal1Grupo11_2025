import json
import uuid


def test_create_store_success(client, headers):
    store_data = {
        "name": "Test Store",
        "phone": "1234567890",
        "email": "test@test.com",
        "address": "Test Address",
        "capacity": 100,
        "state": "ACTIVE",
        "security_level": "HIGH"
    }

    response = client.post('/stores/', json=store_data, headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data['name'] == store_data['name']
    assert data['email'] == store_data['email']
    assert 'id' in data


def test_create_store_duplicate_email(client, headers):
    store_data = {
        "name": "Test Store",
        "phone": "1234567890",
        "email": "duplicate@test.com",
        "address": "Test Address",
        "capacity": 100,
        "state": "ACTIVE",
        "security_level": "HIGH"
    }

    response = client.post('/stores/', json=store_data, headers=headers)
    assert response.status_code == 201

    response = client.post('/stores/', json=store_data, headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'Email already exists'


def test_get_store_by_id_success(client, headers):
    store_data = {
        "name": "Test Store",
        "phone": "1234567890",
        "email": "get@test.com",
        "address": "Test Address",
        "capacity": 100,
        "state": "ACTIVE",
        "security_level": "HIGH"
    }

    response = client.post('/stores/', json=store_data, headers=headers)
    created_store = json.loads(response.data)

    response = client.get(f'/stores/{created_store["id"]}', headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['id'] == created_store['id']
    assert data['name'] == store_data['name']


def test_get_store_invalid_id(client, headers):
    response = client.get('/stores/invalid-uuid', headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'Invalid store id'


def test_get_store_not_found(client, headers):
    random_uuid = str(uuid.uuid4())
    response = client.get(f'/stores/{random_uuid}', headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Store not found'


def test_create_store_invalid_schema(client, headers):
    invalid_store_data = {
        "name": "Test Store",
    }

    response = client.post('/stores/', json=invalid_store_data, headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'message' in data


def test_create_store_db_integrity_error(client, headers):
    store_data = {
        "name": "Test Store",
        "phone": "1234567890",
        "email": "test@test.com",
        "address": "Test Address",
        "capacity": 99999999999999999999999999999999999999999999999999,
        "state": "ACTIVE",
        "security_level": "HIGH"
    }

    response = client.post('/stores/', json=store_data, headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 409
    assert 'message' in data


def test_unauthorized_access(client):
    response = client.get('/stores/123', headers={'Content-Type': 'application/json'})
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'authorization required'


def test_invalid_token(client):
    headers = {
        'x-token': 'invalid_token',
        'Content-Type': 'application/json'
    }

    response = client.get('/stores/123', headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'authorization required'


def test_all_states(client, headers):
    response = client.get('/stores/all-states', headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == 2
    assert 'ACTIVE' in data
    assert 'INACTIVE' in data


def test_all_security_levels(client, headers):
    response = client.get('/stores/all-security-levels', headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == 3
    assert 'LOW' in data
    assert 'MEDIUM' in data
    assert 'HIGH' in data