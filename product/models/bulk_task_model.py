import uuid

from datetime import datetime
from ..models.Operations import BULK_STATUS
from sqlalchemy import DateTime, UUID, Enum

from ..config.db import db

class BulkTask(db.Model):
    __tablename__ = "bulk_tasks"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.String(256), nullable=True)
    file_id = db.Column(db.String(256), nullable=False)
    status = db.Column(Enum(BULK_STATUS), nullable=False)
    created_at = db.Column(DateTime(), default=datetime.now)
    updated_at = db.Column(DateTime(), default=datetime.now)

    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': self.user_id,
            'file_id': self.file_id,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }