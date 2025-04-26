from faker import Faker
from massive_worker.infrastructure.attempt_repository import AttemptRepository
from massive_worker.models.attempt import Attempt
from massive_worker.models.declarative_base import session


class TestAttemptRepository:
    def setup_method(self):
        self.data_factory = Faker()
        self.process_id = str(self.data_factory.uuid4())
        self.file_id = str(self.data_factory.uuid4())
        self.user_id = str(self.data_factory.uuid4())
        
        session.rollback()  # Roll back any previous transactions
        session.query(Attempt).delete()  # Clear the table
        session.commit()
    
    def test_create_attempt_success(self):
        operation = "CREATE"
        entity = "PRODUCT"
        
        attempt = AttemptRepository.create_attempt(
            operation, entity, self.process_id, self.file_id, self.user_id
        )

        assert attempt is not False
        assert attempt.operation.value == operation
        assert attempt.entity.value == entity
        assert str(attempt.process_id) == self.process_id
        assert str(attempt.file_id) == self.file_id
        assert str(attempt.user_id) == self.user_id

    def test_create_attempt_exception(self):
        operation = "BAD_OPERATION"
        entity = "PRODUCT"
        
        attempt_response = AttemptRepository.create_attempt(
            operation, entity, self.process_id, self.file_id, self.user_id
        )

        assert isinstance(attempt_response, bool)
        assert attempt_response is False
