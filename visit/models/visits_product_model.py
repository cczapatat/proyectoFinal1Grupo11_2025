import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, event, DDL
from sqlalchemy.dialects.postgresql import UUID

from ..config.db import db

event.listen(
    db.Model.metadata,
    'before_create',
    DDL('CREATE SCHEMA IF NOT EXISTS visits')
)


class VisitProduct(db.Model):
    __tablename__ = 'visit_products'
    __table_args__ = (
        {'schema': 'visits'}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    visit_id = Column(UUID(as_uuid=True), ForeignKey('visits.visits.id'), nullable=False)
    product_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now)

    def to_dict(self):
        return {
            'id': str(self.id),
            'visit_id': str(self.visit_id),
            'product_id': str(self.product_id),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
