from faker import Faker
import massive_worker.init_bd
from massive_worker.infrastructure.entity_batch_repository import EntityBatchRepository
from massive_worker.models.attempt_error import AttemptError

class TestEntityBatchRepository:
    def setup_method(self):
        self.data_factory = Faker()
        self.process_id = str(self.data_factory.uuid4())
        self.file_id = str(self.data_factory.uuid4())
        self.user_id = str(self.data_factory.uuid4())
    
    def test_create_entity_type_success(self):
        entity_type = "PRODUCT"
        future = '1'
        current_batch = 1
        number_of_batches = 10

        entity_batch = EntityBatchRepository.create_entity_batch(
            entity_type=entity_type,
            process_id=self.process_id,
            file_id=self.file_id,
            user_id=self.user_id,
            future=future,
            current_batch=current_batch,
            number_of_batches=number_of_batches
        )
        assert entity_batch is not False
        assert entity_batch.entity_type == entity_type
        assert str(entity_batch.process_id) == self.process_id
        assert str(entity_batch.file_id) == self.file_id
        assert str(entity_batch.user_id) == self.user_id
        assert entity_batch.future == future
        assert entity_batch.current_batch == current_batch
        assert entity_batch.number_of_batches == number_of_batches
    
    def test_create_entity_type_failure(self):
        entity_type = "PRODUCT"
        process_id = "bad_process_id"
        future = '1'
        current_batch = 1
        number_of_batches = 10

        entity_batch = EntityBatchRepository.create_entity_batch(
            entity_type=entity_type,
            process_id=process_id,
            file_id=self.file_id,
            user_id=self.user_id,
            future=future,
            current_batch=current_batch,
            number_of_batches=number_of_batches
        )
        assert entity_batch is False
    
    def test_get_last_entity_batch_success(self):
        entity_type = "PRODUCT"
        future = '1'
        current_batch = 1
        number_of_batches = 10

        entity_batch = EntityBatchRepository.create_entity_batch(
            entity_type=entity_type,
            process_id=self.process_id,
            file_id=self.file_id,
            user_id=self.user_id,
            future=future,
            current_batch=current_batch,
            number_of_batches=number_of_batches
        )
        assert entity_batch is not False

        last_entity_batch = EntityBatchRepository.get_last_entity_batch(self.process_id)
        assert last_entity_batch is not False
        assert last_entity_batch.entity_type == entity_type
        assert str(last_entity_batch.process_id) == self.process_id
    
    def test_get_last_entity_batch_failure(self):
        process_id = "bad_process_id"
        last_entity_batch = EntityBatchRepository.get_last_entity_batch(process_id)
        assert last_entity_batch is False