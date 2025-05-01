from sqlalchemy.exc import SQLAlchemyError
from .base_command import BaseCommand
from ..errors.errors import ApiError
from ..models.Models import Manufacturer


class GetAllManufacturer(BaseCommand):
    def __init__(self):
        super().__init__()

    def execute(self):
        return self._handle_query(lambda: [manufacturer.to_dict() for manufacturer in Manufacturer.query.all()])

    def _handle_query(self, query_func):
        try:
            return query_func()
        except SQLAlchemyError as e:
            raise ApiError(e)