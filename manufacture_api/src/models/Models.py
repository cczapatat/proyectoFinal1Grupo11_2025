from datetime import datetime
import enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()

class BulkTask(db.Model):
    __tablename__ = "bulk_tasks"
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    user_email = db.Column(db.String(256), nullable=True)
    file_id = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(256), nullable=False)
    createdAt = db.Column(DateTime, nullable=False)
    updatedAt = db.Column(DateTime, nullable=False)

class BulkTaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BulkTask
        load_instance = True
    id = fields.String()

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
    UNITED_KINGDOM = 'UNITED KINGDOM'

class Manufacturer(db.Model):
    __tablename__ = "manufacturers"
    __table_args__ = (
        db.UniqueConstraint('phone', name='unique_manufacturer_phone'),
        db.UniqueConstraint('email', name='unique_manufacturer_email'),
        db.CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'",
            name='valid_manufacturer_email_format'
        ),
        db.CheckConstraint(
            "phone ~* '^\\+[1-9][0-9]{1,14}$'",
            name='valid_manufacturer_phone_format'
        ),
        db.CheckConstraint(
            "rating_quality >= 0",
            name='positive_manufacturer_rating_quality_expected'
        ),

    )
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    country = db.Column(db.Enum(MANUFACTURER_COUNTRY), nullable=False)
    tax_conditions = db.Column(db.String(255), nullable=False)
    legal_conditions = db.Column(db.String(255), nullable=False)
    rating_quality = db.Column(db.Integer, nullable=False)
    created_at = db.Column(DateTime(), default=datetime.now)
    updated_at = db.Column(DateTime(), default=datetime.now)

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

class ManufacturerTaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Manufacturer
        load_instance = True
    id = fields.String()