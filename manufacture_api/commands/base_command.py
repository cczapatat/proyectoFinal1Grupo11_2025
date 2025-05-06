from abc import ABC, abstractmethod

from sqlalchemy.exc import SQLAlchemyError

from ..errors.errors import ApiError


class BaseCommand(ABC):
    @abstractmethod
    def execute(self):  # pragma: no cover
        raise NotImplementedError("Please implement in subclass")

    def handle_query(self, query_func):
        try:
            return query_func()
        except SQLAlchemyError as e:
            raise ApiError(e)
