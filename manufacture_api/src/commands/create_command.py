from datetime import datetime
import traceback
import uuid

from sqlalchemy.exc import SQLAlchemyError
from models.BulkTask import db, BulkTask
from errors.errors import ApiError
from .base_command import BaseCommand
from utilities.publisher_service import PublisherService

class CreateBulkTask(BaseCommand):
    def __init__(self, user_email, bulk_file_url):
        self.id = uuid.uuid4()
        self.user_email = user_email
        self.bulk_file_url = bulk_file_url
        self.status = 'CREATED'
        self.createdAt = datetime.utcnow()
        self.updatedAt = datetime.utcnow()
        self.publisher_service = PublisherService()

    def execute(self):
        try:
            new_bulk_task = BulkTask(
                id=self.id,
                user_email=self.user_email,
                bulk_file_url=self.bulk_file_url,
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
                bulk_file_url=self.bulk_file_url,
                creation_time=self.createdAt,
            )
            self.status = 'BULK QUEUED' if published_ok else 'FAILED'

            return {
                'id': str(self.id),
                'user_email': self.user_email,
                'bulk_file_url': self.bulk_file_url,
                'status': self.status,
                'createdAt': self.createdAt.replace(microsecond=0).isoformat(),
            }
        except SQLAlchemyError as e:
            db.session.rollback()
            traceback.print_exc()
            raise ApiError(e)