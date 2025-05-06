import os
import traceback
import uuid
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from .base_command import BaseCommand
from ..errors.errors import ApiError
from ..models.Models import db, BulkTask
from ..models.Operations import BULK_STATUS
from ..utilities.publisher_service import PublisherService

project_id = os.environ.get('GCP_PROJECT_ID', 'proyectofinalmiso2025')
topic_id = os.environ.get('GCP_PRODUCT_MASSIVE_TOPIC', 'commands_to_massive')
publisher_service = PublisherService(project_id, topic_id)

class CreateBulkTask(BaseCommand):
    def __init__(self, user_id, file_id):
        self.id = uuid.uuid4()
        self.user_id = user_id
        self.file_id = file_id
        self.status = BULK_STATUS.BULK_QUEUED
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.publisher_service = publisher_service

    def execute(self):
        try:
            new_bulk_task = BulkTask(
                id=self.id,
                user_id=self.user_id,
                file_id=self.file_id,
                status=self.status,
                created_at=self.created_at,
                updated_at=self.created_at
            )
            db.session.add(new_bulk_task)
            db.session.commit()

            # Publish synchronously
            published_ok = self.publisher_service.publish_create_command(
                process_id=self.id,
                user_id=self.user_id,
                file_id=self.file_id,
                creation_time=self.created_at,
            )
            self.status = 'BULK QUEUED' if published_ok else 'FAILED'

            return {
                'id': str(self.id),
                'user_id': self.user_id,
                'file_id': self.file_id,
                'status': self.status,
                'createdAt': self.created_at.replace(microsecond=0).isoformat(),
            }
        
        except SQLAlchemyError as e:
            db.session.rollback()
            traceback.print_exc()
            raise ApiError(e)