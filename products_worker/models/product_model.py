import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, Float, Boolean, CheckConstraint, UUID

from .declarative_base import Base

class CURRENCY_PRODUCT(enum.Enum):
    USD = 'USD'
    COP = 'COP'
    EUR = 'EUR'
    GBP = 'GBP'
    ARS = 'ARS'

class CATEGORY_PRODUCT(enum.Enum):
    ELECTRONICS = "ELECTRONICS"
    FURNITURE = "FURNITURE"
    CLOTHING = "CLOTHING"
    FOOD = "FOOD"
    TOYS = "TOYS"
    BOOKS = "BOOKS"
    BEAUTY = "BEAUTY"
    SPORTS = "SPORTS"
    AUTOMOTIVE = "AUTOMOTIVE"
    HEALTH = "HEALTH"
    


class Product(Base):
    __tablename__ = 'products'
    __table_args__ = (
        CheckConstraint(
            "unit_price > 0",
            name='positive_product_currency_price'
        ),
        CheckConstraint(
            "discount_price >= 0",
            name='positive_product_discount_price'
        ),
        CheckConstraint(
            "url_photo ~* '^(https?:\/\/)?([\\da-z.-]+)\\.([a-z.]{2,6})([\/\\w .-]*)*\/?$'",
            name='valid_product_url_photo_format'
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manufacturer_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    category = Column(Enum(CATEGORY_PRODUCT), nullable=False)
    unit_price = Column(Float, nullable=False)
    currency_price = Column(Enum(CURRENCY_PRODUCT), nullable=False)
    is_promotion = Column(Boolean, nullable=False)
    discount_price = Column(Float, nullable=False)
    expired_at = Column(DateTime())
    url_photo = Column(String(255))
    store_conditions = Column(String(255))
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now)