import json
import os
import uuid

import requests_mock

from monitor.config.db import db
from monitor.consumer.stock_update import read_messages
from monitor.models.alarm_trigger import AlarmTrigger

user_session_manager_path = os.getenv('USER_SESSION_MANAGER_PATH', default='http://localhost:3008')

manufacture_id = str(uuid.uuid4())
product_id = str(uuid.uuid4())

alarm_data_mock = {
    "manufacture_id": manufacture_id,
    "product_id": product_id,
    "minimum_value": 10,
    "maximum_value": 100,
    "notes": "Test alarm notes"
}


class MockMessage:
    def __init__(self, data):
        self.data = data

    def ack(self):
        pass


def test_unauthorized_access(client):
    response = client.post('/monitor/new', headers={'Content-Type': 'application/json'}, json=alarm_data_mock)
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'x-token required'


def test_invalid_token(client):
    headers = {
        'x-token': 'invalid_token',
        'Content-Type': 'application/json'
    }

    response = client.post('/monitor/new', headers=headers, json=alarm_data_mock)
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'x-token required'


def test_create_alarm_missing_auth(client, headers):
    response = client.post('/monitor/new', headers=headers, json=alarm_data_mock)
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'authorization required'


def test_create_alarm_invalid_auth(client, headers):
    headers['Authorization'] = 'Bearer invalid_token'
    with requests_mock.Mocker() as m:
        m.get(f'{user_session_manager_path}/user_sessions/auth', status_code=401)
        response = client.post('/monitor/new', headers=headers, json=alarm_data_mock)
        data = json.loads(response.data)

    assert response.status_code == 401
    assert data['message'] == 'authorization required'


def test_create_alarm_invalid_auth_error(client, headers):
    headers['Authorization'] = 'Bearer invalid_token'
    with requests_mock.Mocker() as m:
        m.get(f'{user_session_manager_path}/user_sessions/auth', status_code=404)
        response = client.post('/monitor/new', headers=headers, json=alarm_data_mock)
        data = json.loads(response.data)

    assert response.status_code == 500
    assert data['message'] == 'internal server error on user_session_manager'


def test_create_alarm_missing_values(client, headers):
    headers['Authorization'] = 'Bearer valid_token'
    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': str(uuid.uuid4()),
            'user_type': 'ADMIN'
        })

        alarm_data = {
            "manufacture_id": manufacture_id,
            "product_id": product_id,
            "notes": "Test alarm notes"
        }
        response = client.post('/monitor/new', headers=headers, json=alarm_data)
        data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'minimum_value or maximum_value is required'


def test_create_alarm_integrity_bd(client, headers):
    headers['Authorization'] = 'Bearer valid_token'
    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': str(uuid.uuid4()),
            'user_type': 'ADMIN'
        })

        alarm_data = {
            "manufacture_id": manufacture_id,
            "product_id": product_id,
            "maximum_value": 99999999999999999999999999999999999999999999999999,
            "notes": "Test alarm notes"
        }
        response = client.post('/monitor/new', headers=headers, json=alarm_data)
        data = json.loads(response.data)

    assert response.status_code == 409
    assert data['message'] == 'Database integrity error. 9h9h'


def test_create_alarm_success(client, headers):
    headers['Authorization'] = 'Bearer valid_token'
    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': str(uuid.uuid4()),
            'user_type': 'ADMIN'
        })

        response = client.post('/monitor/new', headers=headers, json=alarm_data_mock)
        data = json.loads(response.data)

    assert response.status_code == 201
    assert 'id' in data
    assert 'created_at' in data
    assert 'updated_at' in data
    assert data['manufacture_id'] == manufacture_id
    assert data['product_id'] == product_id
    assert data['minimum_value'] == alarm_data_mock['minimum_value']
    assert data['maximum_value'] == alarm_data_mock['maximum_value']
    assert data['notes'] == alarm_data_mock['notes']


def test_create_alarm_success_only_minimum_value(client, headers):
    headers['Authorization'] = 'Bearer valid_token'
    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': str(uuid.uuid4()),
            'user_type': 'ADMIN'
        })

        alarm_data = {
            "manufacture_id": manufacture_id,
            "product_id": product_id,
            "minimum_value": 10,
            "notes": "Test alarm notes"
        }
        response = client.post('/monitor/new', headers=headers, json=alarm_data)
        data = json.loads(response.data)

    assert response.status_code == 201
    assert 'id' in data
    assert 'created_at' in data
    assert 'updated_at' in data
    assert data['manufacture_id'] == manufacture_id
    assert data['product_id'] == product_id
    assert data['minimum_value'] == 10
    assert data['maximum_value'] is None
    assert data['notes'] == 'Test alarm notes'


def test_create_alarm_success_only_maximum_value(client, headers):
    headers['Authorization'] = 'Bearer valid_token'
    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': str(uuid.uuid4()),
            'user_type': 'ADMIN'
        })

        alarm_data = {
            "manufacture_id": manufacture_id,
            "product_id": product_id,
            "maximum_value": 100,
            "notes": "Test alarm notes"
        }
        response = client.post('/monitor/new', headers=headers, json=alarm_data)
        data = json.loads(response.data)

    assert response.status_code == 201
    assert 'id' in data
    assert 'created_at' in data
    assert 'updated_at' in data
    assert data['manufacture_id'] == manufacture_id
    assert data['product_id'] == product_id
    assert data['minimum_value'] is None
    assert data['maximum_value'] == 100
    assert data['notes'] == 'Test alarm notes'


def test_create_alarm_success_alarm_trigger_success(client, headers, mock_firebase):
    headers['Authorization'] = 'Bearer valid_token'
    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': str(uuid.uuid4()),
            'user_id': str(uuid.uuid4()),
            'user_type': 'ADMIN'
        })

        alarm_data = {
            "manufacture_id": manufacture_id,
            "product_id": product_id,
            "minimum_value": 300,
            "maximum_value": 350,
            "notes": "Test alarm notes"
        }
        response = client.post('/monitor/new', headers=headers, json=alarm_data)
        data = json.loads(response.data)

    assert response.status_code == 201
    assert 'id' in data

    read_messages(
        MockMessage(data=json.dumps(
            {'product_id': str(product_id), 'stock_unit': 340, 'stock_id': str(uuid.uuid4())}
        ).encode('utf-8'))
    )

    alarm_trigger = db.session.query(AlarmTrigger).filter(AlarmTrigger.product_id == product_id).all()
    assert len(alarm_trigger) == 0
    assert mock_firebase['reference'].call_count == 1

    read_messages(
        MockMessage(data=json.dumps(
            {'product_id': str(product_id), 'stock_unit': 380, 'stock_id': str(uuid.uuid4())}
        ).encode('utf-8'))
    )

    alarm_trigger = db.session.query(AlarmTrigger).filter(AlarmTrigger.product_id == product_id).all()
    assert len(alarm_trigger) == 1
    assert mock_firebase['reference'].call_count == 2
