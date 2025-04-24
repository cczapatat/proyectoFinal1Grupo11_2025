import datetime
from typing import Union
from ..models.entity_batch import OPERATION_BATCH, EntityBatch
from ..models.declarative_base import session


class EntityBatchRepository:
    @staticmethod
    def create_entity_batch(entity_type, process_id, file_id, user_id, future, current_batch, number_of_batches):
        try:
            entity_batch = EntityBatch(
                entity_type=entity_type,
                operation=OPERATION_BATCH.EXECUTED,
                process_id=process_id,
                file_id=file_id,
                user_id=user_id,
                future=future,
                current_batch=current_batch,
                number_of_batches=number_of_batches,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
            )
            session.add(entity_batch)
            session.commit()
            return entity_batch
         
                
        except Exception as ex:
            session.rollback()
            print(f"[EntityBatchRepository] Error creating entity_batch: {ex}")
            return False
    
    @staticmethod
    def get_last_entity_batch(process_id) -> Union[EntityBatch, bool]:
        try:
            return session.query(EntityBatch).filter_by(process_id=process_id).order_by(EntityBatch.created_at.desc()).first() or False
        except Exception as ex:
            print(f"[Get Last Entity Batch] process_id: {process_id}, error: {str(ex)}")

            return False