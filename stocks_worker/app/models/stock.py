import uuid
import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import Base

class Stock(Base):
    __tablename__ = "stocks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_name = Column(String, nullable=False)
    quantity_in_stock = Column(Integer, nullable=False)
    last_quantity = Column(Integer, nullable=True)
    enabled = Column(Boolean, default=True)
    update_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)