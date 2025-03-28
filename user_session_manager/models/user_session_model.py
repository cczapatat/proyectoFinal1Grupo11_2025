import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, UniqueConstraint, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID

from ..config.db import db


class TYPE(enum.Enum):
    SELLER = 'SELLER'
    ADMIN = 'ADMIN'
    CLIENT = 'CLIENT'

class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    __table_args__ = (
        UniqueConstraint('email', name='unique_user_session_email'),
        CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'",
            name='valid_user_session_email_format'
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    type = Column(Enum(TYPE), nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now)

    def to_dict(self):
        return {
            'id': str(self.id),
            'email': self.email,
            'type': self.type.value,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }