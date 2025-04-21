import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, DateTime, UUID

from .declarative_base import Base


class OPERATION_BATCH(enum.Enum):
    EXECUTED = 'EXECUTED'
    ##UPDATE = 'update'
    ##DELETE = 'delete'


class EntityBatch(Base):
    __tablename__ = 'entity_batches'
    __table_args__ = {'schema': 'massive_worker'}  

    id = Column(Integer(), primary_key=True)
    entity_type = Column(String(255), nullable=False)
    operation = Column(Enum(OPERATION_BATCH), nullable=False)
    file_id = Column(String(255), nullable=False)
    process_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    user_id = Column(String(255), nullable=False)
    future = Column(String(255), nullable=False)
    current_batch = Column(Integer(), nullable=False)
    number_of_batches = Column(Integer(), nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now)