import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, event, DDL, Text, Integer, Index
from sqlalchemy.dialects.postgresql import UUID

from ..config.db import db

event.listen(
    db.Model.metadata,
    'before_create',
    DDL('CREATE SCHEMA IF NOT EXISTS monitor')
)


class Alarm(db.Model):
    __tablename__ = 'alarms'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255), nullable=False)
    manufacture_id = Column(UUID(as_uuid=True), nullable=False)
    product_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    minimum_value = Column(Integer, nullable=True)
    maximum_value = Column(Integer, nullable=True)
    notes = Column(Text, nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now)

    __table_args__ = (
        Index('idx_alarms_manufacture_id_product_id', 'manufacture_id', 'product_id', postgresql_using="btree"),
        {'schema': 'monitor'},
    )

    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'manufacture_id': str(self.manufacture_id),
            'product_id': str(self.product_id),
            'minimum_value': self.minimum_value,
            'maximum_value': self.maximum_value,
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
