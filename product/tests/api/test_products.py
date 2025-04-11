import json

from faker import Faker

from product import application as app
from product.models.product_model import CATEGORY_PRODUCT, CURRENCY_PRODUCT


class TestProduct:
    def setup_method(self):
        self.data_factory = Faker()
        self.test_client = app.test_client()

    def _generate_product_data(self, **overrides):
        product_data = {
            "manufacturer_id": str(self.data_factory.uuid4()),
            "name": self.data_factory.word(),
            "description": self.data_factory.word(),
            "category": "ELECTRONICS",
            "unit_price": 100.0,
            "currency_price": "USD",
            "is_promotion": True,
            "discount_price": 10.0,
            "expired_at": (self.data_factory.future_datetime()).isoformat(),
            "url_photo": self.data_factory.image_url(),
            "store_conditions": self.data_factory.text(max_nb_chars=50)
        }
        product_data.update(overrides)
        return product_data

    def _post_product(self, product_data):
        return self.test_client.post(
            '/products/create',
            data=json.dumps(product_data),
            headers={
                'x-token': 'internal_token',
                'content-type': 'application/json'
            }
        )

    def _put_product(self, product_data, productId):
        return self.test_client.put(
            f'/products/update/{productId}',
            data=json.dumps(product_data),
            headers={
                'x-token': 'internal_token',
                'content-type': 'application/json'
            }
        )

    def test_health_check(self):
        response = self.test_client.get('/products/health')

        assert response.status_code == 200

        json_response = json.loads(response.data)
        assert json_response['status'] == 'up'

    def test_create_product_error_missing_token(self):
        product_data = self._generate_product_data()

        response = self.test_client.post(
            '/products/create',
            data=json.dumps(product_data),
            headers={'content-type': 'application/json'}
        )

        assert response.status_code == 401

    def test_create_product_error_invalid_token(self):
        product_data = self._generate_product_data()

        response = self.test_client.post(
            '/products/create',
            data=json.dumps(product_data),
            headers={
                'x-token': 'bad_token',
                'content-type': 'application/json'
            }
        )

        assert response.status_code == 401

    def test_create_product_error_missing_field(self):
        required_fields = [
            "manufacturer_id", "name", "description", "category",
            "unit_price", "currency_price", "is_promotion",
            "discount_price", "url_photo", "store_conditions"
        ]

        for field in required_fields:
            product_data = self._generate_product_data()
            product_data.pop(field)

            response = self._post_product(product_data)

            assert response.status_code == 400

            json_response = json.loads(response.data)
            assert json_response['message'] == f'{field} is required'

    def test_create_product_error_invalid_category(self):
        product_data = self._generate_product_data(category="BAD_CATEGORY")

        response = self._post_product(product_data)

        assert response.status_code == 500

    def test_create_product_error_invalid_unit_price(self):
        product_data = self._generate_product_data(unit_price=-100.0)

        response = self._post_product(product_data)

        assert response.status_code == 400

    def test_create_product_error_invalid_currency_price(self):
        product_data = self._generate_product_data(currency_price="BAD_CURRENCY")

        response = self._post_product(product_data)

        assert response.status_code == 500

    def test_create_product_error_invalid_format_expired_at(self):
        product_data = self._generate_product_data(expired_at="BAD_DATE")

        response = self._post_product(product_data)

        assert response.status_code == 400

    def test_crerate_product_error_expired_at_in_past(self):
        product_data = self._generate_product_data(expired_at=(self.data_factory.past_datetime()).isoformat())

        response = self._post_product(product_data)

        assert response.status_code == 400

    def test_create_product_error_invalid_url_photo(self):
        product_data = self._generate_product_data(url_photo="BAD_URL")

        response = self._post_product(product_data)

        assert response.status_code == 400

    def test_create_product_success(self):
        product_data = self._generate_product_data()

        response = self._post_product(product_data)

        assert response.status_code == 201

        json_response = json.loads(response.data)
        assert json_response['id'] is not None

    def test_create_product_without_expired_at_success(self):
        product_data = self._generate_product_data()
        product_data.pop('expired_at')

        response = self._post_product(product_data)

        assert response.status_code == 201

        json_response = json.loads(response.data)
        assert json_response['id'] is not None

    def test_update_product_error_missing_field(self):
        product_data = self._generate_product_data()
        product_response = self._post_product(product_data)

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
            print(f'product: {product}')
            product.pop(field)

            response = self._put_product(product, productId)

            assert response.status_code == 400

            json_response = json.loads(response.data)
            assert json_response['message'] == f'{field} is required'

    def test_update_product_success(self):
        product_data = self._generate_product_data()
        product_response = self._post_product(product_data)

        assert product_response.status_code == 201

        product_data = json.loads(product_response.data)
        productId = str(product_data['id'])
        product = json.loads(product_response.data)

        nameUpdated = self.data_factory.word()
        product['name'] = nameUpdated

        response = self._put_product(product, productId)

        assert response.status_code == 200
        json_response = json.loads(response.data)
        assert json_response['id'] == productId
        assert json_response['name'] == nameUpdated

    def test_update_product_error_invalid_product_id(self):
        product_data = self._generate_product_data()
        product_response = self._post_product(product_data)
        productId = self.data_factory.uuid4()

        assert product_response.status_code == 201

        product_data = json.loads(product_response.data)
        product = json.loads(product_response.data)

        nameUpdated = self.data_factory.word()
        product['name'] = nameUpdated

        response = self._put_product(product, productId)

        assert response.status_code == 404

    def test_update_product_error_past_expired_at(self):
        product_data = self._generate_product_data()
        product_response = self._post_product(product_data)

        assert product_response.status_code == 201

        product_data = json.loads(product_response.data)
        productId = str(product_data['id'])
        product = json.loads(product_response.data)

        expired_at = (self.data_factory.past_datetime()).isoformat()
        product['expired_at'] = expired_at

        response = self._put_product(product, productId)

        assert response.status_code == 400

    def test_update_product_error_invalid_format_expired_at(self):
        product_data = self._generate_product_data()
        product_response = self._post_product(product_data)

        assert product_response.status_code == 201

        product_data = json.loads(product_response.data)
        productId = str(product_data['id'])
        product = json.loads(product_response.data)

        expired_at = "BAD_DATE"
        product['expired_at'] = expired_at

        response = self._put_product(product, productId)

        assert response.status_code == 400

    def test_update_product_error_integrity_error(self):
        product_data = self._generate_product_data()
        product_response = self._post_product(product_data)

        assert product_response.status_code == 201

        product_data = json.loads(product_response.data)
        productId = str(product_data['id'])
        product = json.loads(product_response.data)

        product['unit_price'] = -100.0

        response = self._put_product(product, productId)

        assert response.status_code == 400

    def test_update_product_error_internal_server_error(self):
        product_data = self._generate_product_data()
        product_response = self._post_product(product_data)

        assert product_response.status_code == 201

        product_data = json.loads(product_response.data)
        productId = str(product_data['id'])
        product = json.loads(product_response.data)

        product['currency_price'] = "BAD_CURRENCY"

        response = self._put_product(product, productId)

        assert response.status_code == 500

    def test_get_product(self):
        product_data = self._generate_product_data()
        product_response = self._post_product(product_data)

        assert product_response.status_code == 201

        product_data = json.loads(product_response.data)
        productId = str(product_data['id'])

        response = self.test_client.get(f'/products/get/{productId}', headers={
            'x-token': 'internal_token',
            'content-type': 'application/json'
        })

        assert response.status_code == 200

        json_response = json.loads(response.data)
        assert json_response is not None
        assert json_response['id'] == productId

    def test_get_product_error_invalid_product_id(self):
        product_data = self._generate_product_data()
        product_response = self._post_product(product_data)

        assert product_response.status_code == 201

        product_data = json.loads(product_response.data)
        productId = self.data_factory.uuid4()

        response = self.test_client.get(f'/products/get/{productId}', headers={
            'x-token': 'internal_token',
            'content-type': 'application/json'
        })

        assert response.status_code == 404

    def test_get_all_products(self):
        product_data = self._generate_product_data()
        product_response = self._post_product(product_data)

        assert product_response.status_code == 201

        product_data = json.loads(product_response.data)

        response = self.test_client.get('/products/list', headers={
            'x-token': 'internal_token',
            'content-type': 'application/json'
        })

        assert response.status_code == 200
    
    def test_get_products_paginated(self):
        product_data = self._generate_product_data()
        product_response = self._post_product(product_data)

        assert product_response.status_code == 201

        product_data = json.loads(product_response.data)

        response = self.test_client.get('/products/list', headers={
            'x-token': 'internal_token',
            'content-type': 'application/json',
            'page': 1,
            'per_page' : 2
        })

        assert response.status_code == 200

    def test_get_all_categories(self):
        response = self.test_client.get('/products/categories', headers={
            'x-token': 'internal_token',
            'content-type': 'application/json'
        })

        assert response.status_code == 200

        json_response = json.loads(response.data)
        assert json_response is not None
        assert len(json_response) == CATEGORY_PRODUCT.__len__()

    def test_get_all_currencies(self):
        response = self.test_client.get('/products/currencies', headers={
            'x-token': 'internal_token',
            'content-type': 'application/json'
        })

        assert response.status_code == 200

        json_response = json.loads(response.data)
        assert json_response is not None
        assert len(json_response) == CURRENCY_PRODUCT.__len__()

    def test_get_products_by_ids_missing(self):
        response = self.test_client.post('/products/by-ids', headers={
            'x-token': 'internal_token',
            'content-type': 'application/json'
        }, json={})
        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['message'] == 'ids is required'

    def test_get_products_by_ids_wrong(self):
        response = self.test_client.post('/products/by-ids', headers={
            'x-token': 'internal_token',
            'content-type': 'application/json'
        }, json={'ids': {}})
        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['message'] == 'ids must be a list'

    def test_get_products_by_ids_empty(self):
        response = self.test_client.post('/products/by-ids', headers={
            'x-token': 'internal_token',
            'content-type': 'application/json'
        }, json={'ids': []})
        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['message'] == 'ids cannot be empty'

    def test_get_products_by_ids_invalid(self):
        response = self.test_client.post('/products/by-ids', headers={
            'x-token': 'internal_token',
            'content-type': 'application/json'
        }, json={'ids': [
            'invalid_id'
        ]})
        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['message'] == 'invalids product ids'

    def test_get_products_by_ids_success(self):
        product_data_one = self._generate_product_data()
        product_response_one = self._post_product(product_data_one)
        assert product_response_one.status_code == 201
        product_data_one = json.loads(product_response_one.data)
        product_id_one = str(product_data_one['id'])

        product_data_two = self._generate_product_data()
        product_response_two = self._post_product(product_data_two)
        assert product_response_two.status_code == 201
        product_data_two = json.loads(product_response_two.data)
        product_id_two = str(product_data_two['id'])

        response = self.test_client.post('/products/by-ids', headers={
            'x-token': 'internal_token',
            'content-type': 'application/json'
        }, json={'ids': [product_id_one, product_id_two]})
        data = json.loads(response.data)

        assert response.status_code == 200
        assert len(data) == 2

        response_cached = self.test_client.post('/products/by-ids', headers={
            'x-token': 'internal_token',
            'content-type': 'application/json'
        }, json={'ids': [product_id_one, product_id_two]})
        data_cached = json.loads(response_cached.data)

        assert response_cached.status_code == 200
        assert data == data_cached
