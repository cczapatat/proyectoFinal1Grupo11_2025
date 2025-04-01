import random
from faker import Faker
from src.models.Models import MANUFACTURER_COUNTRY
from src.main import app


class TestManufacturerBluePrint:
    def setup_method(self):
        self.data_factory = Faker()
        self.token = 'internal_token'

    def _generate_manufacturer_payload(self, **overrides):
        payload = {
            "name": self.data_factory.name(),
            "address": self.data_factory.address(),
            "phone": '+5730054367' + str(self.data_factory.random_int(min=1000, max=9999)),
            "email": self.data_factory.email(),
            "country": random.choice(list(MANUFACTURER_COUNTRY)).value,
            "tax_conditions": self.data_factory.word(),
            "legal_conditions": self.data_factory.word(),
            "rating_quality": self.data_factory.random_int(min=1, max=5),
        }
        payload.update(overrides)
        return payload

    def _post_create_manufacturer(self, payload, token=None):
        with app.test_client() as test_client:
            return test_client.post(
                '/manufacture-api/manufacturers/create',
                headers={'x-token': token or self.token},
                json=payload
            )

    def test_create_manufacturer_fail_unauthorized(self):
        payload = self._generate_manufacturer_payload()
        response = self._post_create_manufacturer(payload, token=self.data_factory.word())

        assert response.status_code == 401
    
    def test_create_manufacturer_fail_bad_token(self):
        self.token = None
        payload = self._generate_manufacturer_payload(token=self.token)
        response = self._post_create_manufacturer(payload)

        assert response.status_code == 401

    def test_create_manufacturer_fail_phone_number(self):
        payload = self._generate_manufacturer_payload(phone=self.data_factory.word())
        response = self._post_create_manufacturer(payload)

        assert response.status_code == 500

    def test_create_manufacturer_fail_email(self):
        payload = self._generate_manufacturer_payload(email=self.data_factory.word())
        response = self._post_create_manufacturer(payload)

        assert response.status_code == 500

    def test_create_manufacturer_fail_rating(self):
        payload = self._generate_manufacturer_payload(rating_quality=-20)
        response = self._post_create_manufacturer(payload)

        assert response.status_code == 500

    def test_create_manufacturer_fail_country(self):
        payload = self._generate_manufacturer_payload(country=self.data_factory.word())
        response = self._post_create_manufacturer(payload)

        assert response.status_code == 500

    def test_create_manufacturer_success(self):
        payload = self._generate_manufacturer_payload()
        response = self._post_create_manufacturer(payload)

        assert response.status_code == 201
        assert response.json['id'] is not None
        assert response.json['name'] == payload['name']
    
    def test_get_all_manufacturer_success(self):
        with app.test_client() as test_client:
            response = test_client.get(
                '/manufacture-api/manufacturers/all',
                headers={'x-token': self.token}
            )
            assert response.status_code == 200
            assert isinstance(response.json, list)