import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID

from ..config.db import db


class Stock(db.Model):
    __tablename__ = 'stocks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_product = Column(UUID(as_uuid=True), nullable=False)
    id_store = Column(UUID(as_uuid=True), nullable=False)
    quantity_in_stock = Column(Integer(), nullable=True, default=0)
    last_quantity = Column(Integer(), nullable=True, default=0)
    enabled = Column(Boolean(), default=True)
    update_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    creation_date = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': str(self.id),
            'id_product': str(self.id_product),
            "id_store": str(self.id_store),
            'quantity_in_stock': int(self.quantity_in_stock),
            'last_quantity': int(self.last_quantity),
            'enabled': self.enabled,
            'update_date': self.update_date.strftime('%Y-%m-%d %H:%M:%S'),
            'creation_date': self.creation_date.strftime('%Y-%m-%d %H:%M:%S'),
        }
