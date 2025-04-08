import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Numeric, Enum, event, DDL
from sqlalchemy.dialects.postgresql import UUID

from .enums import PAYMENT_METHOD, ORDER_STATE
from .order_product_model import OrderProduct
from ..config.db import db

event.listen(
    db.Model.metadata,
    'before_create',
    DDL('CREATE SCHEMA IF NOT EXISTS orders')
)


class Order(db.Model):
    __tablename__ = 'orders'
    __table_args__ = (
        {'schema': 'orders'}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255), nullable=False)
    seller_id = Column(UUID(as_uuid=True), nullable=False)
    client_id = Column(UUID(as_uuid=True), nullable=False)
    delivery_date = Column(DateTime(), nullable=False)
    payment_method = Column(Enum(PAYMENT_METHOD), nullable=False)
    total_amount = Column(Numeric, nullable=False)
    state = Column(Enum(ORDER_STATE), nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now)

    def to_dict(self, products: list[OrderProduct]):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'seller_id': str(self.seller_id),
            'client_id': str(self.client_id),
            'delivery_date': self.delivery_date.strftime('%Y-%m-%d %H:%M:%S'),
            'payment_method': self.payment_method.name,
            'total_amount': int(self.total_amount),
            'state': self.state.name,
            'products': [product.to_dict() for product in products],
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
