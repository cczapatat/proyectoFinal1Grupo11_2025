import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, event, DDL, Text
from sqlalchemy.dialects.postgresql import UUID

from .visits_product_model import VisitProduct
from ..config.db import db

event.listen(
    db.Model.metadata,
    'before_create',
    DDL('CREATE SCHEMA IF NOT EXISTS visits')
)


class Visit(db.Model):
    __tablename__ = 'visits'
    __table_args__ = (
        {'schema': 'visits'}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255), nullable=False)
    seller_id = Column(UUID(as_uuid=True), nullable=False)
    client_id = Column(UUID(as_uuid=True), nullable=False)
    description = Column(Text, nullable=False)
    visit_date = Column(DateTime(), nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now)

    def to_dict(self, products: list[VisitProduct]):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'seller_id': str(self.seller_id),
            'client_id': str(self.client_id),
            'description': self.description,
            'visit_date': self.visit_date.strftime('%Y-%m-%d %H:%M:%S'),
            'products': [product.to_dict() for product in products],
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
