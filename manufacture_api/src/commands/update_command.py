from .base_command import BaseCommand
from errors.errors import ApiError
from models.BulkTask import db, BulkTask
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import traceback


class BulkTaskUpdate(BaseCommand):
    def __init__(self, id: int, status: str):
        self.id = id
        self.status = status

    def execute(self) -> BulkTask:
        try:
            bulk_task_update = BulkTask.query.filter_by(id=self.id).first()
            if not bulk_task_update:
                raise ApiError("BulkTask not found")

            bulk_task_update.status = self.status
            bulk_task_update.updatedAt = datetime.now()

            db.session.commit()
            return bulk_task_update
        except SQLAlchemyError as e:
            db.session.rollback()
            traceback.print_exc()
            raise ApiError(str(e))
        except Exception as e:
            db.session.rollback()
            traceback.print_exc()
            raise ApiError("An unexpected error occurred: " + str(e))