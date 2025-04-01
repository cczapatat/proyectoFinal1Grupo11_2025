import random
from faker import Faker
from src.main import app


class TestBulkTaskBluePrint:
    def setup_method(self):
        self.data_factory = Faker()
        self.token = 'internal_token'

    def _generate_bulk_task_payload(self, **overrides):
        payload = {
            "user_email": self.data_factory.email(),
            "file_id": self.data_factory.uuid4(),
        }
        payload.update(overrides)
        return payload

    def _post_create_bulk_task(self, payload, token=None):
        with app.test_client() as test_client:
            return test_client.post(
                '/manufacture-api/bulk',
                headers={'x-token': token or self.token},
                json=payload
            )

    def _get_bulk_task_by_user_email(self, user_email, token=None):
        with app.test_client() as test_client:
            return test_client.get(
                f'/manufacture-api/bulk/user?user_email={user_email}',
                headers={'x-token': token or self.token}
            )
    
    def _get_bulk_task_by_user_id(self, id, token=None):
        with app.test_client() as test_client:
            return test_client.get(
                f'/manufacture-api/bulk/user?id={id}',
                headers={'x-token': token or self.token}
            )

    def test_create_bulk_task_fail_unauthorized(self):
        payload = self._generate_bulk_task_payload()
        response = self._post_create_bulk_task(payload, token=self.data_factory.word())

        assert response.status_code == 401

    def test_create_bulk_task_success(self):
        payload = self._generate_bulk_task_payload()
        response = self._post_create_bulk_task(payload)

        assert response.status_code == 201
        assert response.json['id'] is not None
        assert response.json['user_email'] == payload['user_email']
    
    def test_filter_bulk_task_by_user_id_success(self):
        payload = self._generate_bulk_task_payload()
        bulk_task = self._post_create_bulk_task(payload)

        response = self._get_bulk_task_by_user_id(bulk_task.json['id'])

        assert response.status_code == 200

    def test_filter_bulk_task_by_user_email_success(self):
        user_email = self.data_factory.email()
        payload = self._generate_bulk_task_payload(user_email=user_email)
        self._post_create_bulk_task(payload)

        response = self._get_bulk_task_by_user_email(user_email)

        assert response.status_code == 200
        assert len(response.json) > 0
        assert response.json[0]['user_email'] == user_email

    def test_filter_bulk_task_by_user_email_not_found(self):
        user_email = self.data_factory.email()
        response = self._get_bulk_task_by_user_email(user_email)

        assert response.status_code == 200
        assert len(response.json) == 0