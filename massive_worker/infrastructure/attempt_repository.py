import datetime
from typing import Union

from ..models.attempt import Attempt
from ..models.declarative_base import session


class AttemptRepository:
    @staticmethod
    def create_attempt(operation, entity, process_id, file_id, user_id):
        try:
            attempt = Attempt(
                operation=operation.upper(),
                entity=entity.upper(),
                process_id=process_id,
                file_id=file_id,
                user_id=user_id,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
            )
            session.add(attempt)
            session.commit()
            return attempt
                
        except Exception as ex:
            session.rollback()
            print(f"[AttemptRepository] Error creating attempt: {ex}")
            return False
    
   