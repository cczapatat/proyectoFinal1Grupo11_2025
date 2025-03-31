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
