import os
import traceback
import uuid
from datetime import datetime

from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

from .base_command import BaseCommand
from ..errors.errors import ApiError
from ..models.Models import db, BulkTask
from ..models.Operations import BULK_STATUS
from ..utilities.publisher_service import PublisherService

project_id = os.environ.get('GCP_PROJECT_ID', 'proyectofinalmiso2025')
topic_id = os.environ.get('GCP_PRODUCT_MASSIVE_TOPIC', 'commands_to_massive')
publisher_service = PublisherService(project_id, topic_id)

class CreateMassiveManufacturer(BaseCommand):
    def __init__(self, user_id, file_id):
        self.id = uuid.uuid4()
        self.user_id = user_id
        self.file_id = file_id
        self.status = BULK_STATUS.BULK_QUEUED
        self.createdAt = datetime.utcnow()
        self.updatedAt = datetime.utcnow()
        self.publisher_service = publisher_service

    def execute(self):
        try:
            new_bulk_task = BulkTask(
                id=self.id,
                user_id=self.user_id,
                file_id=self.file_id,
                status=self.status,
                created_at=self.createdAt,
                updated_at=self.updatedAt
            )
            db.session.add(new_bulk_task)
            db.session.commit()

            published_ok = self.publisher_service.publish_create_command(
                process_id=self.id,
                user_id=self.user_id,
                file_id=self.file_id,
                creation_time=self.createdAt,
            )

            if not published_ok:
                new_bulk_task.status = BULK_STATUS.BUlK_FAILED
                return jsonify(new_bulk_task.to_dict()), 500

            return jsonify(new_bulk_task.to_dict()), 201
        
        except SQLAlchemyError as e:
            db.session.rollback()
            traceback.print_exc()
            raise ApiError(e)