from faker import Faker
import massive_worker.init_bd
from massive_worker.infrastructure.attempt_error_repository import AttemptErrorRepository
from massive_worker.models.attempt_error import AttemptError
from massive_worker.models.declarative_base import session

class TestAttemptErrorRepository:
    def setup_method(self):
        self.data_factory = Faker()
        self.process_id = str(self.data_factory.uuid4())
        self.file_id = str(self.data_factory.uuid4())
        self.user_id = str(self.data_factory.uuid4())
        session.rollback()
        session.query(AttemptError).delete()
        session.commit()
    
    def test_create_attempt_error_success(self):
        operation = "CREATE"
        entity = "PRODUCT"
        retry_quantity = 1
        
        attemptError = AttemptErrorRepository.create_attempt_error(
            operation, entity, self.process_id, self.file_id, self.user_id, retry_quantity
        )

        assert attemptError is not False
        assert attemptError.operation.value == operation
        assert attemptError.entity.value == entity
        assert str(attemptError.process_id) == self.process_id
        assert str(attemptError.file_id) == self.file_id
        assert str(attemptError.user_id) == self.user_id

    def test_create_attempt_error_exception(self):
        operation = "BAD_OPERATION"
        entity = "PRODUCT"
        retry_quantity = 1

        attemp_error_response = AttemptErrorRepository.create_attempt_error(
            operation, entity, self.process_id, self.file_id, self.user_id, retry_quantity
        )

        assert isinstance(attemp_error_response, bool)
        assert attemp_error_response is False
    
    def test_get_last_attempt_error_success(self):
        operation = "CREATE"
        entity = "PRODUCT"
        retry_quantity = 1

        attemptError = AttemptErrorRepository.create_attempt_error(
            operation, entity, self.process_id, self.file_id, self.user_id, retry_quantity
        )

        last_attempt_error = AttemptErrorRepository.get_last_attempt_error(self.process_id)

        assert last_attempt_error is not False
        assert last_attempt_error.operation.value == operation
        assert last_attempt_error.entity.value == entity
        assert str(last_attempt_error.process_id) == self.process_id
        assert str(last_attempt_error.file_id) == self.file_id
        assert str(last_attempt_error.user_id) == self.user_id
    
    def test_get_last_attempt_error_exception(self):
        process_id = "BAD_PROCESS_ID"
        last_attempt_error = AttemptErrorRepository.get_last_attempt_error(process_id)
        assert last_attempt_error is False
