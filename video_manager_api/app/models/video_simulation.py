import uuid
import datetime
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import Base


class VideoSimulation(Base):
    __tablename__ = 'video_simulations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    store_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    file_path = Column(String(), nullable=False)
    tags = Column(String(), nullable=True)
    enabled = Column(Boolean(), default=True)
    update_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': str(self.id),
            'document_id': str(self.document_id),
            'store_id': str(self.store_id),
            'file_path': self.file_path,
            'tags': self.tags,
            'enabled': self.enabled,
            'update_date': self.update_date.strftime('%Y-%m-%d %H:%M:%S'),
            'creation_date': self.creation_date.strftime('%Y-%m-%d %H:%M:%S'),
        }
