from datetime import datetime

from ..models.bulk_task_model import BulkTask
from ..models.declarative_base import session

class BulkTaskRepository:

    @staticmethod
    def update_bulk_task_status(bulk_task_id: str, status: str):
        try:
            bulk_task = session.query(BulkTask).filter(BulkTask.id == bulk_task_id).first()
            if bulk_task is not None:
                bulk_task.status = status
                bulk_task.updated_at = datetime.now()
                session.commit()
                return bulk_task
            else:
                print(f"[Update Bulk Task] id: {bulk_task_id}, error: BulkTask not found")
                return False
        except Exception as ex:
            session.rollback()
            print(f"[Update Bulk Task] id: {bulk_task_id}, error: {ex}")
            return False
