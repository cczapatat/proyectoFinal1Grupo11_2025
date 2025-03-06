import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID

from ..config.db import db


class Stock(db.Model):
    __tablename__ = 'stocks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_name = Column(String(255), nullable=False)
    quantity_in_stock = Column(Integer(), nullable=False)
    last_quantity = Column(Integer(), nullable=False)
    enabled = Column(Boolean(), default=False)
    update_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    creation_date = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': str(self.id),
            'product_name': self.product_name,
            'quantity_in_stock': int(self.quantity_in_stock),
            'last_quantity': int(self.last_quantity),
            'enabled': self.enabled,
            'update_date': self.update_date.strftime('%Y-%m-%d %H:%M:%S'),
            'creation_date': self.creation_date.strftime('%Y-%m-%d %H:%M:%S'),
        }
