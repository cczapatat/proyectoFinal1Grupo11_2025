import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, event, DDL, Integer, Text
from sqlalchemy.dialects.postgresql import UUID

from ..config.db import db

event.listen(
    db.Model.metadata,
    'before_create',
    DDL('CREATE SCHEMA IF NOT EXISTS monitor')
)


class AlarmTrigger(db.Model):
    __tablename__ = 'alarms_trigger'
    __table_args__ = (
        {'schema': 'monitor'},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alarm_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    stock_id = Column(String(255), nullable=False)
    product_id = Column(String(255), nullable=False, index=True)
    minimum_value = Column(Integer, nullable=True)
    maximum_value = Column(Integer, nullable=True)
    new_stock_unit = Column(Integer, nullable=True)
    notes = Column(Text, nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now)
