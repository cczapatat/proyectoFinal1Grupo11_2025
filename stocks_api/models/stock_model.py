import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Numeric, Boolean
from sqlalchemy.dialects.postgresql import UUID

from ..config.db import db


class Stock(db.Model):
    __tablename__ = 'stocks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_name = Column(String(255), nullable=False)
    quantity_in_stock = Column(Numeric(), nullable=False)
    last_quantity = Column(Numeric(), nullable=False)
    enabled = Column(Boolean(), nullable=False)
    update_date = Column(DateTime(), default=datetime.now)
    creation_date = Column(DateTime(), default=datetime.now)

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
