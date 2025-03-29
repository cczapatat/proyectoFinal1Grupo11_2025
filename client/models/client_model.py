import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, UniqueConstraint, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..config.db import db

class CLIENT_TYPE(enum.Enum):
    CORNER_STORE = "CORNER_STORE"
    SUPERMARKET = "SUPERMARKET"

class VENDOR_ZONE(enum.Enum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"
    CENTER = "CENTER"
    NORTHEAST = "NOTRHEAST"
    NORTHWEST = "NORTHWEST"
    SOUTHEAST = "SOUTHEAST"
    SOUTHWEST = "SOUTHWEST"


class Client(db.Model):
    __tablename__ = 'clients'
    __table_args__ = (
        UniqueConstraint('user_id', name='unique_client_user_id'),
        UniqueConstraint('phone', name='unique_client_phone'),
        UniqueConstraint('email', name='unique_client_email'),
        CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'",
            name='valid_client_email_format'
        ),
        CheckConstraint(
            "phone ~* '^\\+[1-9][0-9]{1,14}$'",
            name='valid_client_phone_format'
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    client_type = Column(Enum(CLIENT_TYPE), nullable=False)
    zone = Column(Enum(VENDOR_ZONE), nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now)

    seller_association = relationship("ClientSeller", back_populates="client")

    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'client_type': self.client_type.value,
            'zone': self.zone.value,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }