from faker import Faker
from products_worker.infrastructure.bulk_task_repository import BulkTaskRepository
from products_worker.models.Operations import BULK_STATUS
from products_worker.models.bulk_task_model import BulkTask
from products_worker.models.declarative_base import session


class TestBulkTaskRepository:
    def setup_method(self):
        self.data_factory = Faker()
        session.rollback()
        session.query(BulkTask).delete()

        self.bulk_task = BulkTask(
            user_id=str(self.data_factory.uuid4()),
            file_id=str(self.data_factory.uuid4()),
            status=BULK_STATUS.BULK_QUEUED,
            created_at=self.data_factory.date_time(),
            updated_at=self.data_factory.date_time()
        )

        session.add(self.bulk_task)
        session.commit()
        self.process_id = str(self.bulk_task.id)


    def test_update_bulk_task_status_success(self):
        new_status = BULK_STATUS.BULK_COMPLETED
        bulk_task = BulkTaskRepository.update_bulk_task_status(self.bulk_task.id, new_status)

        assert bulk_task is not False
        assert bulk_task.status == new_status
    
    def test_update_bulk_task_status_not_found(self):
        new_status = BULK_STATUS.BULK_COMPLETED
        bulk_task = BulkTaskRepository.update_bulk_task_status(str(self.data_factory.uuid4()), new_status)

        assert bulk_task is False
    
    def test_update_bulk_task_status_exception(self):
        new_status = "BAD_STATUS"
        bulk_task = BulkTaskRepository.update_bulk_task_status(self.bulk_task.id, new_status)

        assert bulk_task is False
