from datetime import datetime
import os
import traceback
import uuid

from models.Operations import Status
from sqlalchemy.exc import SQLAlchemyError
from models.Models import db, BulkTask
from errors.errors import ApiError
from .base_command import BaseCommand
from utilities.publisher_service import PublisherService

class CreateBulkTask(BaseCommand):
    def __init__(self, user_email, file_id):
        self.id = uuid.uuid4()
        self.user_email = user_email
        self.file_id = file_id
        self.status = Status.BULK_QUEUED.value
        self.createdAt = datetime.utcnow()
        self.updatedAt = datetime.utcnow()
        self.publisher_service = PublisherService(os.getenv("GCP_PROJECT_ID"), os.getenv("GCP_MANUFACTURE_MASSIVE_TOPIC"))

    def execute(self):
        try:
            new_bulk_task = BulkTask(
                id=self.id,
                user_email=self.user_email,
                file_id=self.file_id,
                status=self.status,
                createdAt=self.createdAt,
                updatedAt=self.updatedAt
            )
            db.session.add(new_bulk_task)
            db.session.commit()

            # Publish synchronously
            published_ok = self.publisher_service.publish_create_command(
                process_id=self.id,
                user_email=self.user_email,
                file_id=self.file_id,
                creation_time=self.createdAt,
            )
            self.status = 'BULK QUEUED' if published_ok else 'FAILED'

            return {
                'id': str(self.id),
                'user_email': self.user_email,
                'file_id': self.file_id,
                'status': self.status,
                'createdAt': self.createdAt.replace(microsecond=0).isoformat(),
            }
        
        except SQLAlchemyError as e:
            db.session.rollback()
            traceback.print_exc()
            raise ApiError(e)