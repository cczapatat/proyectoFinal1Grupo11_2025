import uuid
import datetime
import enum
from sqlalchemy import Column, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import Base

class UpdateStatus(enum.Enum):
    COMMITTED = "COMMITTED"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"
    RECEIVED = "RECEIVED"

class UpdateStockAttempt(Base):
    __tablename__ = "update_stock_attempts"
    transaction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    last_update_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(Enum(UpdateStatus), nullable=False)