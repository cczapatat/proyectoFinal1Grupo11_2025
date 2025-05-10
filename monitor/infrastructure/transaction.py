from typing import Callable

from ..config.db import db


class Transaction:
    @staticmethod
    def run(function: Callable[[], any]) -> any:
        try:
            db.session.begin_nested()
            result = function()
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e
