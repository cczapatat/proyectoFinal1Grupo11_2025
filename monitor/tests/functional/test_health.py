import json


def test_health_check(client):
    response = client.get('/monitor/health')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['status'] == 'up'
