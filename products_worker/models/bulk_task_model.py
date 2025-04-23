import uuid
from datetime import datetime
from products_worker.models.Operations import BULK_STATUS
from sqlalchemy import Column, DateTime, String, UUID, Enum

from .declarative_base import Base

class BulkTask(Base):
    __tablename__ = "bulk_tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(256), nullable=True)
    file_id = Column(String(256), nullable=False)
    status = Column(Enum(BULK_STATUS), nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now)