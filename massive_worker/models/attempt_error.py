from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, DateTime, UUID

from .declarative_base import Base
from .attempt import OPERATION, ENTITY

class AttemptError(Base):
    __tablename__ = 'attempt_errors'
    __table_args__ = {'schema': 'massive_worker'}  

    id = Column(Integer(), primary_key=True)
    operation = Column(Enum(OPERATION), nullable=False)
    entity = Column(Enum(ENTITY), nullable=False)
    file_id = Column(String(255), nullable=False)
    process_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    user_id = Column(String(255), nullable=False)
    retry_quantity = Column(Integer(), default=0)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now)