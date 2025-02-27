from sqlalchemy.exc import SQLAlchemyError
from .base_command import BaseCommand
from errors.errors import ApiError
from models.BulkTask import BulkTask


class FilterBulkTaskByUserEmail(BaseCommand):
    def __init__(self, user_email):
        self.user_email = user_email

    def execute(self):
        return self._handle_query(lambda: BulkTask.query.filter(BulkTask.user_email == self.user_email).all())

    def _handle_query(self, query_func):
        try:
            return query_func()
        except SQLAlchemyError as e:
            raise ApiError(e)


class FilterBulkTaskById(BaseCommand):
    def __init__(self, id):
        self.id = id

    def execute(self):
        return self._handle_query(self._get_bulk_task_by_id)

    def _get_bulk_task_by_id(self):
        result = BulkTask.query.filter_by(id=self.id).first()
        if result is None:
            raise ApiError("BulkTask not found")
        return result

    def _handle_query(self, query_func):
        try:
            return query_func()
        except SQLAlchemyError as e:
            raise ApiError(e)