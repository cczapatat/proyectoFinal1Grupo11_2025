import json

from uuid import uuid4


def test_create_client_success(client, headers):
    client_data = {
        "user_id": str(uuid4()),
        "seller_id": str(uuid4()),
        "name": "Test Client",
        "phone": "+573017084751",
        "email": "test@example.com",
        "address": "Test Address 123",
        "client_type": "CORNER_STORE",
        "zone": "NORTH"

    }

    response = client.post('/clients/create', json=client_data, headers=headers)
    data = json.loads(response.data)
    print(response)
    assert response.status_code == 201
    assert data['name'] == client_data['name']
    assert data['email'] == client_data['email']
    assert 'id' in data



def test_create_client_duplicate_email(client, headers):
    client_data_one = {
        "user_id": str(uuid4()),
        "seller_id": str(uuid4()),
        "name": "Test Client",
        "phone": "+573017084752",
        "email": "duplicate@example.com",
        "address": "Test Address 122",
        "client_type": "CORNER_STORE",
        "zone": "NORTH"
    }
    client_data_two = {
        "user_id": str(uuid4()),
        "seller_id": str(uuid4()),
        "name": "Test Client",
        "phone": "+573017084753",
        "email": "duplicate@example.com",
        "address": "Test Address 122",
        "client_type": "CORNER_STORE",
        "zone": "NORTH"
    }

    response = client.post('/clients/create', json=client_data_one, headers=headers)
    assert response.status_code == 201

    response = client.post('/clients/create', json=client_data_two, headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'Email already exists'


def test_create_client_duplicate_user_id(client, headers):
    user_id = uuid4()
    client_data_one = {
        "user_id": str(user_id),
        "seller_id": str(uuid4()),
        "name": "Test Client",
        "phone": "+5730170848",
        "email": "userid@example.com",
        "address": "Test Address 122",
        "client_type": "CORNER_STORE",
        "zone": "NORTH"
    }
    client_data_two = {
        "user_id": str(user_id),
        "seller_id": str(uuid4()),
        "name": "Test Client",
        "phone": "+5730170847",
        "email": "userid2@example.com",
        "address": "Test Address 122",
        "client_type": "CORNER_STORE",
        "zone": "NORTH"
    }
    print(client_data_one)
    response = client.post('/clients/create', json=client_data_one, headers=headers)
    assert response.status_code == 201

    response = client.post('/clients/create', json=client_data_two, headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'Client already exists'

def test_create_client_duplicate_phone(client, headers):
    client_data_one = {
        "user_id": str(uuid4()),
        "seller_id": str(uuid4()),
        "name": "Test Client",
        "phone": "+5730170841",
        "email": "duplicate20@example.com",
        "address": "Test Address 122",
        "client_type": "CORNER_STORE",
        "zone": "NORTH"
    }
    client_data_two = {
        "user_id": str(uuid4()),
        "seller_id": str(uuid4()),
        "name": "Test Client",
        "phone": "+5730170841",
        "email": "duplicate10@example.com",
        "address": "Test Address 123",
        "client_type": "CORNER_STORE",
        "zone": "NORTH"
    }

    response = client.post('/clients/create', json=client_data_one, headers=headers)
    assert response.status_code == 201

    response = client.post('/clients/create', json=client_data_two, headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'Phone already exists'


def test_create_client_bad_email(client, headers):
    client_data_one = {
        "user_id": str(uuid4()),
        "seller_id": str(uuid4()),
        "name": "Test Client",
        "phone": "+573017084752",
        "email": "userid.com",
        "address": "Test Address 122",
        "client_type": "CORNER_STORE",
        "zone": "NORTH"
    }


    response = client.post('/clients/create', json=client_data_one, headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'Email format is not valid'

def test_create_client_bad_phone(client, headers):
    client_data_one = {
        "user_id": str(uuid4()),
        "seller_id": str(uuid4()),
        "name": "Test Client",
        "phone": "+573017084752a",
        "email": "userid@gmail.com",
        "address": "Test Address 122",
        "client_type": "CORNER_STORE",
        "zone": "NORTH"
    }


    response = client.post('/clients/create', json=client_data_one, headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'Phone format is not valid'

def test_get_client_by_id_success(client, headers):
    client_data = {
        "user_id": str(uuid4()),
        "seller_id": str(uuid4()),
        "name": "Test Client",
        "phone": "+57301708473",
        "email": "test30@example.com",
        "address": "Test Address 123",
        "client_type": "CORNER_STORE",
        "zone": "NORTH"

    }

    response = client.post('/clients/create', json=client_data, headers=headers)
    created_client = json.loads(response.data)

    response = client.get(f'/clients/{created_client["user_id"]}', headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['user_id'] == created_client['user_id']
    assert data['name'] == client_data['name']

def test_get_client_client_not_found(client, headers):
    response = client.get(f'/clients/{str(uuid4())}', headers=headers)
    data = json.loads(response.data)
    assert response.status_code == 404
    assert data['message'] == 'client not found'

def test_get_client_invalid_id(client, headers):
    response = client.get(f'/clients/invalid-id', headers=headers)
    data = json.loads(response.data)
    print(data)
    assert response.status_code == 409
    assert 'Database integrity error.' in data['message']

def test_create_client_db_integrity_error(client, headers):
    client_data = {
        "user_id": '123456',
        "seller_id": str(uuid4()),
        "name": "Test Client",
        "phone": "+57301708473",
        "email": "test30@example.com",
        "address": "Test Address 123",
        "client_type": "CORNER_STORE",
        "zone": "NORTH"
    }

    response = client.post('/clients/create', json=client_data, headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 409
    assert 'message' in data

def test_unauthorized_access(client):
    response = client.get(f'/clients/{str(uuid4())}', headers={'Content-Type': 'application/json'})
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'authorization required'


def test_invalid_token(client):
    headers = {
        'x-token': 'invalid_token',
        'Content-Type': 'application/json'
    }

    response = client.get(f'/clients/{str(uuid4())}', headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'authorization required'