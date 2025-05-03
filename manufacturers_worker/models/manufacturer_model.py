import enum
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, Integer, CheckConstraint, UUID, UniqueConstraint

from .declarative_base import Base

class MANUFACTURER_COUNTRY (enum.Enum):
    USA = 'USA'
    CANADA = 'CANADA'
    MEXICO = 'MEXICO'
    BRAZIL = 'BRAZIL'
    ARGENTINA = 'ARGENTINA'
    CHILE = 'CHILE'
    COLOMBIA = 'COLOMBIA'
    PERU = 'PERU'
    VENEZUELA = 'VENEZUELA'
    UNITED_KINGDOM = 'UNITED_KINGDOM'


class Manufacturer(Base):
    __tablename__ = "manufacturers"
    __table_args__ = (
        UniqueConstraint('phone', name='unique_manufacturer_phone'),
        UniqueConstraint('email', name='unique_manufacturer_email'),
        CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'",
            name='valid_manufacturer_email_format'
        ),
        CheckConstraint(
            "phone ~* '^\\+[1-9][0-9]{1,14}$'",
            name='valid_manufacturer_phone_format'
        ),
        CheckConstraint(
            "rating_quality >= 0",
            name='positive_manufacturer_rating_quality_expected'
        ),

    )
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    country = Column(Enum(MANUFACTURER_COUNTRY), nullable=False)
    tax_conditions = Column(String(255), nullable=False)
    legal_conditions = Column(String(255), nullable=False)
    rating_quality = Column(Integer, nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now)

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'country': self.country.value,
            'tax_conditions': self.tax_conditions,
            'legal_conditions': self.legal_conditions,
            'rating_quality': self.rating_quality,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }