import json
import os
import requests_mock

from unittest.mock import MagicMock, Mock, patch
from faker import Faker
from product.models.product_model import CATEGORY_PRODUCT, CURRENCY_PRODUCT

user_session_manager_path = os.getenv('USER_SESSION_MANAGER_PATH', default='http://localhost:3008')
data_factory = Faker()

def _generate_product_data(**overrides):
    product_data = {
        "manufacturer_id": str(data_factory.uuid4()),
        "name": data_factory.word(),
        "description": data_factory.word(),
        "category": "ELECTRONICS",
        "unit_price": 100.0,
        "currency_price": "USD",
        "is_promotion": True,
        "discount_price": 10.0,
        "expired_at": (data_factory.future_datetime()).isoformat(),
        "url_photo": data_factory.image_url(),
        "store_conditions": data_factory.text(max_nb_chars=50)
    }
    product_data.update(overrides)
    return product_data

def _post_product(client, product_data):
    return client.post(
        '/products/create',
        data=json.dumps(product_data),
        headers={
            'x-token': 'internal_token',
            'content-type': 'application/json'
        }
    )

def _put_product(client, product_data, productId):
    return client.put(
        f'/products/update/{productId}',
        data=json.dumps(product_data),
        headers={
            'x-token': 'internal_token',
            'content-type': 'application/json'
        }
    )

def test_health_check(client):
    response = client.get('/products/health')

    assert response.status_code == 200

    json_response = json.loads(response.data)
    assert json_response['status'] == 'up'

def test_create_product_error_missing_token(client):
    product_data = _generate_product_data()

    response = client.post(
        '/products/create',
        data=json.dumps(product_data),
        headers={'content-type': 'application/json'}
    )

    assert response.status_code == 401

def test_create_product_error_invalid_token(client):
    product_data = _generate_product_data()

    response = client.post(
        '/products/create',
        data=json.dumps(product_data),
        headers={
            'x-token': 'bad_token',
            'content-type': 'application/json'
        }
    )

    assert response.status_code == 401

def test_create_product_error_missing_field(client):
    required_fields = [
        "manufacturer_id", "name", "description", "category",
        "unit_price", "currency_price", "is_promotion",
        "discount_price", "url_photo", "store_conditions"
    ]

    for field in required_fields:
        product_data = _generate_product_data()
        product_data.pop(field)

        response = _post_product(client, product_data)

        assert response.status_code == 400

        json_response = json.loads(response.data)
        assert json_response['message'] == f'{field} is required'

def test_create_product_error_invalid_category(client):
    product_data = _generate_product_data(category="BAD_CATEGORY")

    response = _post_product(client, product_data)

    assert response.status_code == 500

def test_create_product_error_invalid_unit_price(client):
    product_data = _generate_product_data(unit_price=-100.0)

    response = _post_product(client, product_data)

    print(f"Response: {response.data}")

    assert response.status_code == 400

def test_create_product_error_invalid_currency_price(client):
    product_data = _generate_product_data(currency_price="BAD_CURRENCY")

    response = _post_product(client, product_data)

    assert response.status_code == 500

def test_create_product_error_invalid_format_expired_at(client):
    product_data = _generate_product_data(expired_at="BAD_DATE")

    response = _post_product(client, product_data)

    assert response.status_code == 400

def test_crerate_product_error_expired_at_in_past(client):
    product_data = _generate_product_data(expired_at=(data_factory.past_datetime()).isoformat())

    response = _post_product(client, product_data)

    assert response.status_code == 400

def test_create_product_error_invalid_url_photo(client):
    product_data = _generate_product_data(url_photo="BAD_URL")

    response = _post_product(client, product_data)

    assert response.status_code == 400

def test_create_product_success(client):
    product_data = _generate_product_data()

    response = _post_product(client, product_data)

    assert response.status_code == 201

    json_response = json.loads(response.data)
    assert json_response['id'] is not None

def test_create_product_without_expired_at_success(client):
    product_data = _generate_product_data()
    product_data.pop('expired_at')

    response = _post_product(client, product_data)

    assert response.status_code == 201

    json_response = json.loads(response.data)
    assert json_response['id'] is not None

def test_update_product_error_missing_field(client):
    product_data = _generate_product_data()
    product_response = _post_product(client, product_data)

    assert product_response.status_code == 201

    product_data = json.loads(product_response.data)
    productId = str(product_data['id'])
    product = json.loads(product_response.data)

    required_fields = [
        "manufacturer_id", "name", "description", "category",
        "unit_price", "currency_price", "is_promotion",
        "discount_price", "url_photo", "store_conditions"
    ]

    for field in required_fields:
        product_data = json.loads(product_response.data)
        productId = str(product_data['id'])
        product = json.loads(product_response.data)
        product.pop(field)

        response = _put_product(client, product, productId)

        assert response.status_code == 400

        json_response = json.loads(response.data)
        assert json_response['message'] == f'{field} is required'

def test_update_product_success(client):
    product_data = _generate_product_data()
    product_response = _post_product(client, product_data)

    assert product_response.status_code == 201

    product_data = json.loads(product_response.data)
    productId = str(product_data['id'])
    product = json.loads(product_response.data)

    nameUpdated = data_factory.word()
    product['name'] = nameUpdated

    response = _put_product(client, product, productId)

    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert json_response['id'] == productId
    assert json_response['name'] == nameUpdated

def test_update_product_error_invalid_product_id(client):
    product_data = _generate_product_data()
    product_response = _post_product(client, product_data)
    productId = data_factory.uuid4()

    assert product_response.status_code == 201

    product_data = json.loads(product_response.data)
    product = json.loads(product_response.data)

    nameUpdated = data_factory.word()
    product['name'] = nameUpdated

    response = _put_product(client, product, productId)

    assert response.status_code == 404


def test_update_product_error_past_expired_at(client):
    product_data = _generate_product_data()
    product_response = _post_product(client, product_data)

    assert product_response.status_code == 201

    product_data = json.loads(product_response.data)
    productId = str(product_data['id'])
    product = json.loads(product_response.data)

    expired_at = (data_factory.past_datetime()).isoformat()
    product['expired_at'] = expired_at

    response = _put_product(client, product, productId)

    assert response.status_code == 400

def test_update_product_error_invalid_format_expired_at(client):
    product_data = _generate_product_data()
    product_response = _post_product(client, product_data)

    assert product_response.status_code == 201

    product_data = json.loads(product_response.data)
    productId = str(product_data['id'])
    product = json.loads(product_response.data)

    expired_at = "BAD_DATE"
    product['expired_at'] = expired_at

    response = _put_product(client, product, productId)

    assert response.status_code == 400

def test_update_product_error_integrity_error(client):
    product_data = _generate_product_data()
    product_response = _post_product(client, product_data)

    assert product_response.status_code == 201

    product_data = json.loads(product_response.data)
    productId = str(product_data['id'])
    product = json.loads(product_response.data)

    product['unit_price'] = -100.0

    response = _put_product(client, product, productId)

    assert response.status_code == 400

def test_update_product_error_internal_server_error(client):
    product_data = _generate_product_data()
    product_response = _post_product(client, product_data)

    assert product_response.status_code == 201

    product_data = json.loads(product_response.data)
    productId = str(product_data['id'])
    product = json.loads(product_response.data)

    product['currency_price'] = "BAD_CURRENCY"

    response = _put_product(client, product, productId)

    assert response.status_code == 500

def test_create_massive_product_without_authorization(client):
    fake_file_id = data_factory.uuid4()

    response = client.post(
        '/products/massive/create',
        data=json.dumps({'file_id': fake_file_id}),
        headers={
            'content-type': 'application/json',
            'x-token': 'internal_token'
        }
    )

    assert response.status_code == 401

def test_create_massive_product_auth_response_unauthorized(client):
    fake_authorization = data_factory.uuid4()
    fake_file_id = data_factory.uuid4()

    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', status_code=401)

        response = client.post(
            '/products/massive/create',
            data=json.dumps({'file_id': fake_file_id}),
            headers={
                'content-type': 'application/json',
                'x-token': 'internal_token',
                'Authorization': fake_authorization
            }
        )
    assert response.status_code == 401

def test_create_massive_product_auth_response_internal_error(client):
    fake_authorization = data_factory.uuid4()
    fake_file_id = data_factory.uuid4()

    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', status_code=500)

        response = client.post(
            '/products/massive/create',
            data=json.dumps({'file_id': fake_file_id}),
            headers={
                'content-type': 'application/json',
                'x-token': 'internal_token',
                'Authorization': fake_authorization
            }
        )
    assert response.status_code == 500


def test_create_massive_products_missing_file_id(client):
    fake_user_id = data_factory.uuid4()
    fake_file_id = data_factory.uuid4()
    fake_authorization = data_factory.uuid4()

    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': fake_user_id,
            'user_id': fake_user_id,
            'user_type': 'SELLER'
        })

        response = client.post(
            '/products/massive/create',
            data=json.dumps({}),
            headers={
                'content-type': 'application/json',
                'x-token': 'internal_token',
                'Authorization': fake_authorization
            }
        )

    assert response.status_code == 400
    json_response = json.loads(response.data)
    assert json_response['message'] == 'file_id is required'

@patch("product.api.products.PublisherService.publish_create_command")
def test_create_massive_products_success_by_seller(mock_pubsub, client):
    fake_user_id = data_factory.uuid4()
    fake_file_id = data_factory.uuid4()
    fake_authorization = data_factory.uuid4()

    mock_pubsub.return_value = True

    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': fake_user_id,
            'user_id': fake_user_id,
            'user_type': 'SELLER'
        })

        response = client.post(
            '/products/massive/create',
            data=json.dumps({'file_id': fake_file_id}),
            headers={
                'content-type': 'application/json',
                'x-token': 'internal_token',
                'Authorization': fake_authorization
            }
        )

    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert json_response['id'] is not None
    mock_pubsub.assert_called_once()

@patch("product.api.products.PublisherService.publish_create_command")
def test_create_massive_products_success_by_admin(mock_pubsub, client):
    fake_user_id = data_factory.uuid4()
    fake_file_id = data_factory.uuid4()
    fake_authorization = data_factory.uuid4()

    mock_pubsub.return_value = True

    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': fake_user_id,
            'user_id': fake_user_id,
            'user_type': 'ADMIN'
        })

        response = client.post(
            '/products/massive/create',
            data=json.dumps({'file_id': fake_file_id}),
            headers={
                'content-type': 'application/json',
                'x-token': 'internal_token',
                'Authorization': fake_authorization
            }
        )

    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert json_response['id'] is not None
    mock_pubsub.assert_called_once()


def test_create_massive_products_forbidden_by_other_user_type(client):
    fake_user_id = data_factory.uuid4()
    fake_file_id = data_factory.uuid4()
    fake_authorization = data_factory.uuid4()

    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': fake_user_id,
            'user_id': fake_user_id,
            'user_type': 'OTHER_TYPE_USER'
        })

        response = client.post(
            '/products/massive/create',
            data=json.dumps({'file_id': fake_file_id}),
            headers={
                'content-type': 'application/json',
                'x-token': 'internal_token',
                'Authorization': fake_authorization
            }
        )

    assert response.status_code == 403
    json_response = json.loads(response.data)
    assert json_response['message'] == 'Invalid user type'

@patch("product.api.products.PublisherService.publish_create_command")
def test_create_massive_products_publish_error(mock_publish_create_command, client):
    fake_user_id = data_factory.uuid4()
    fake_file_id = data_factory.uuid4()
    fake_authorization = data_factory.uuid4()

    mock_publish_create_command.return_value = False

    with requests_mock.Mocker() as m:
        # Mock auth response
        m.get(f'{user_session_manager_path}/user_sessions/auth', json={
            'user_session_id': fake_user_id,
            'user_id': fake_user_id,
            'user_type': 'SELLER'
        })

        response = client.post(
            '/products/massive/create',
            data=json.dumps({'file_id': fake_file_id}),
            headers={
                'content-type': 'application/json',
                'x-token': 'internal_token',
                'Authorization': fake_authorization
            }
        )

        assert response.status_code == 500
        json_response = json.loads(response.data)
        assert json_response['status'] == 'FAILED'

def test_get_product(client):
    product_data = _generate_product_data()
    product_response = _post_product(client, product_data)

    assert product_response.status_code == 201

    product_data = json.loads(product_response.data)
    productId = str(product_data['id'])

    response = client.get(f'/products/get/{productId}', headers={
        'x-token': 'internal_token',
        'content-type': 'application/json'
    })

    assert response.status_code == 200

    json_response = json.loads(response.data)
    assert json_response is not None
    assert json_response['id'] == productId

def test_get_product_error_invalid_product_id(client):
    product_data = _generate_product_data()
    product_response = _post_product(client, product_data)

    assert product_response.status_code == 201

    product_data = json.loads(product_response.data)
    productId = data_factory.uuid4()

    response = client.get(f'/products/get/{productId}', headers={
        'x-token': 'internal_token',
        'content-type': 'application/json'
    })

    assert response.status_code == 404

def test_get_all_products(client):
    product_data = _generate_product_data()
    product_response = _post_product(client, product_data)

    assert product_response.status_code == 201

    product_data = json.loads(product_response.data)

    response = client.get('/products/list', headers={
        'x-token': 'internal_token',
        'content-type': 'application/json'
    })

    assert response.status_code == 200

def test_get_products_paginated(client):
    product_data = _generate_product_data()
    product_response = _post_product(client, product_data)

    assert product_response.status_code == 201

    product_data = json.loads(product_response.data)

    response = client.get('/products/list', headers={
        'x-token': 'internal_token',
        'content-type': 'application/json',
        'page': 1,
        'per_page' : 2
    })

    assert response.status_code == 200

def test_get_all_categories(client):
    response = client.get('/products/categories', headers={
        'x-token': 'internal_token',
        'content-type': 'application/json'
    })

    assert response.status_code == 200

    json_response = json.loads(response.data)
    assert json_response is not None
    assert len(json_response) == CATEGORY_PRODUCT.__len__()

def test_get_all_currencies(client):
    response = client.get('/products/currencies', headers={
        'x-token': 'internal_token',
        'content-type': 'application/json'
    })

    assert response.status_code == 200

    json_response = json.loads(response.data)
    assert json_response is not None
    assert len(json_response) == CURRENCY_PRODUCT.__len__()

def test_get_products_by_ids_missing(client):
    response = client.post('/products/by-ids', headers={
        'x-token': 'internal_token',
        'content-type': 'application/json'
    }, json={})
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'ids is required'

def test_get_products_by_ids_wrong(client):
    response = client.post('/products/by-ids', headers={
        'x-token': 'internal_token',
        'content-type': 'application/json'
    }, json={'ids': {}})
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'ids must be a list'

def test_get_products_by_ids_empty(client):
    response = client.post('/products/by-ids', headers={
        'x-token': 'internal_token',
        'content-type': 'application/json'
    }, json={'ids': []})
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'ids cannot be empty'

def test_get_products_by_ids_invalid(client):
    response = client.post('/products/by-ids', headers={
        'x-token': 'internal_token',
        'content-type': 'application/json'
    }, json={'ids': [
        'invalid_id'
    ]})
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'invalids product ids'

def test_get_products_by_ids_success(client):
    product_data_one = _generate_product_data()
    product_response_one = _post_product(client, product_data_one)
    assert product_response_one.status_code == 201
    product_data_one = json.loads(product_response_one.data)
    product_id_one = str(product_data_one['id'])

    product_data_two = _generate_product_data()
    product_response_two = _post_product(client, product_data_two)
    assert product_response_two.status_code == 201
    product_data_two = json.loads(product_response_two.data)
    product_id_two = str(product_data_two['id'])

    response = client.post('/products/by-ids', headers={
        'x-token': 'internal_token',
        'content-type': 'application/json'
    }, json={'ids': [product_id_one, product_id_two]})
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == 2

    response_cached = client.post('/products/by-ids', headers={
        'x-token': 'internal_token',
        'content-type': 'application/json'
    }, json={'ids': [product_id_one, product_id_two]})
    data_cached = json.loads(response_cached.data)

    assert response_cached.status_code == 200
    assert data == data_cached

def test_get_products_paginated_full(client):
    product_data = _generate_product_data()
    product_response = _post_product(client, product_data)

    assert product_response.status_code == 201

    product_data = json.loads(product_response.data)

    response = client.get('/products/paginated_full', headers={
        'x-token': 'internal_token',
        'content-type': 'application/json',
        'page': 1,
        'per_page' : 2
    })

    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert json_response is not None
    assert len(json_response) == 5