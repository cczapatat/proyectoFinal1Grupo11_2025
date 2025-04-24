import datetime
from typing import Union
from models.attempt_error import AttemptError
from models.declarative_base import session


class AttemptErrorRepository: 
    @staticmethod
    def create_attempt_error(operation, entity, process_id, file_id, user_id, retry_quantity):
        try:
            attempt_error = AttemptError(
                operation=operation,
                entity=entity,
                process_id=process_id,
                file_id=file_id,
                user_id=user_id,
                retry_quantity=retry_quantity,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
            )
            session.add(attempt_error)
            session.commit()
            return attempt_error
        except Exception as ex:
            session.rollback()
            print(f"[AttemptErrorRepository] Error creating attempt error: {ex}")
            return False
    
    @staticmethod
    def get_last_attempt_error(process_id):
        try:
            return session.query(AttemptError).filter_by(process_id=process_id).order_by(AttemptError.created_at.desc()).first() or False
        except Exception as ex:
            print(f"[Get Last Attempt Error] process_id: {process_id}, error: {str(ex)}")
            return False