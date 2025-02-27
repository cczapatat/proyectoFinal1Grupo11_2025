import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, DateTime, UUID

from .declarative_base import Base


class OPERATION(enum.Enum):
    CREATE = 'CREATE'
    ##UPDATE = 'update'
    ##DELETE = 'delete'

class ENTITY(enum.Enum):
    MANUFACTURES = 'MANUFACTURES'
    ##PRODUCTS = 'products'
    ##CLIENTS = 'clients'


class Attempt(Base):
    __tablename__ = 'attempts'
    __table_args__ = {'schema': 'massive_worker'}  

    id = Column(Integer(), primary_key=True)
    operation = Column(Enum(OPERATION), nullable=False)
    entity = Column(Enum(ENTITY), nullable=False)
    file_id = Column(String(255), nullable=False)
    process_id = Column(UUID(as_uuid=True), nullable=False)
    user_email = Column(String(255), nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now)