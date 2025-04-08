import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, event, DDL
from sqlalchemy.dialects.postgresql import UUID

from ..config.db import db

event.listen(
    db.Model.metadata,
    'before_create',
    DDL('CREATE SCHEMA IF NOT EXISTS orders')
)


class OrderProduct(db.Model):
    __tablename__ = 'order_products'
    __table_args__ = (
        {'schema': 'orders'}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.orders.id'), nullable=False)
    product_id = Column(UUID(as_uuid=True), nullable=False)
    units = Column(Integer, nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now)

    def to_dict(self):
        return {
            'id': str(self.id),
            'order_id': str(self.order_id),
            'product_id': str(self.product_id),
            'units': int(self.units),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
