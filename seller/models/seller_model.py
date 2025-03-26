import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, Float, UniqueConstraint, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID

from ..config.db import db


class CURRENCY(enum.Enum):
    USD = 'USD'
    COP = 'COP'
    EUR = 'EUR'
    GBP = 'GBP'
    ARS = 'ARS'

class SELLER_ZONE(enum.Enum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"
    CENTER = "CENTER"
    NORTHEAST = "NOTRHEAST"
    NORTHWEST = "NORTHWEST"
    SOUTHEAST = "SOUTHEAST"
    SOUTHWEST = "SOUTHWEST"
    


class Seller(db.Model):
    __tablename__ = 'sellers'
    __table_args__ = (
        UniqueConstraint('user_id', name='unique_seller_user_id'),
        UniqueConstraint('phone', name='unique_seller_phone'),
        UniqueConstraint('email', name='unique_seller_email'),
        CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'",
            name='valid_seller_email_format'
        ),
        CheckConstraint(
            "phone ~* '^\\+[1-9][0-9]{1,14}$'",
            name='valid_seller_phone_format'
        ),
        CheckConstraint(
            "quota_expected > 0",
            name='positive_seller_quota_expected'
        ),
        CheckConstraint(
            "quartely_target > 0",
            name='positive_seller_quartely_target'
        ),

    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    zone = Column(Enum(SELLER_ZONE), nullable=False)
    quota_expected = Column(Float, nullable=False)
    currency_quota = Column(Enum(CURRENCY), nullable=False)
    quartely_target = Column(Float, nullable=False)
    currency_target = Column(Enum(CURRENCY), nullable=False)
    performance_recomendations = Column(String(255), nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now)

    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'zone': self.zone.value,
            'quota_expected': self.quota_expected,
            'currency_quota': self.currency_quota.value,
            'quartely_target': self.quartely_target,
            'currency_target': self.currency_target.value,
            'performance_recomendations': self.performance_recomendations,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }