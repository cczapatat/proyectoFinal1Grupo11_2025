import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, UniqueConstraint, Enum, event, DDL
from sqlalchemy.dialects.postgresql import UUID

from ..config.db import db
from .enums import STATE, SECURITY_LEVEL

event.listen(
    db.Model.metadata,
    'before_create',
    DDL('CREATE SCHEMA IF NOT EXISTS stores')
)

class Store(db.Model):
    __tablename__ = 'stores'
    __table_args__ = (
        UniqueConstraint('email', name='unique_email'),
        {'schema': 'stores'}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    address = Column(String(500), nullable=False)
    capacity = Column(Integer(), nullable=False)
    state = Column(Enum(STATE), nullable=False)
    security_level = Column(Enum(SECURITY_LEVEL), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'capacity': self.capacity,
            'state': self.state.name,
            'security_level': self.security_level.name,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
