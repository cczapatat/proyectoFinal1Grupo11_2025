import uuid
from datetime import datetime

from flask import jsonify, make_response
from sqlalchemy import asc, desc
from sqlalchemy.exc import IntegrityError

from ..config.db import db
from ..dtos.bulk_task_dto import BulkTaskDTO
from ..models.bulk_task_model import BulkTask


class BulkTaskRepository:

    @staticmethod
    def create_bulk_task(bulk_task_dto: BulkTaskDTO) -> BulkTask:
        bulk_task = BulkTask()
        bulk_task.user_id = bulk_task_dto.user_id
        bulk_task.file_id = bulk_task_dto.file_id
        bulk_task.status = bulk_task_dto.status
        bulk_task.created_at = datetime.now()
        bulk_task.updated_at = datetime.now()

        try:
            db.session.add(bulk_task)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            response = make_response(
                jsonify({"error": "Integrity error", "message": str(e.orig)}), 400
            )
            return response
        except Exception as e:
            db.session.rollback()
            response = make_response(
                jsonify({"error": "Internal server error", "message": str(e)}), 500
            )
            return response

        return bulk_task
