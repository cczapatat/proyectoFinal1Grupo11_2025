import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validates, ValidationError
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import UniqueConstraint
import uuid

db = SQLAlchemy()

# Manufacturer model definition
class Manufacturer(db.Model):
    __tablename__ = "manufacturers"
    # Combine schema specification with constraints
    __table_args__ = (
        UniqueConstraint('nombre', 'nit', name='unique_nombre_nit'),
        {'schema': os.environ.get('DB_SCHEMA', 'manufacturers')}
    )
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = db.Column(db.String(255), nullable=False)
    nit = db.Column(db.String(255), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(255), nullable=False)
    correo = db.Column(db.String(255), nullable=False)
    codigo_pais = db.Column(db.String(2), nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

# Error model definition to store validation errors
class Error(db.Model):
    __tablename__ = "errors"
    __table_args__ = {'schema': os.environ.get('DB_SCHEMA', 'manufacturers')}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_id = db.Column(UUID(as_uuid=True), nullable=False)
    batch_number = db.Column(db.Integer, nullable=False)
    line_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Schema for Manufacturer model
class ManufacturerSchema(SQLAlchemyAutoSchema):
    id = fields.String()
    
    class Meta:
        model = Manufacturer
        load_instance = True
        
    @validates('nombre')
    def validate_nombre(self, value):
        if not value:
            raise ValidationError("nombre is required")
        if len(value) > 255:
            raise ValidationError("nombre must be less than 255 characters")
            
    @validates('nit')
    def validate_nit(self, value):
        if not value:
            raise ValidationError("nit is required")
        if len(value) > 255:
            raise ValidationError("nit must be less than 255 characters")
            
    @validates('direccion')
    def validate_direccion(self, value):
        if not value:
            raise ValidationError("direccion is required")
        if len(value) > 255:
            raise ValidationError("direccion must be less than 255 characters")
            
    @validates('telefono')
    def validate_telefono(self, value):
        if not value:
            raise ValidationError("telefono is required")
        if len(value) > 255:
            raise ValidationError("telefono must be less than 255 characters")
            
    @validates('correo')
    def validate_correo(self, value):
        if not value:
            raise ValidationError("correo is required")
        if len(value) > 255:
            raise ValidationError("correo must be less than 255 characters")
            
    @validates('codigo_pais')
    def validate_codigo_pais(self, value):
        if not value:
            raise ValidationError("codigo_pais is required")
        if len(value) > 2:
            raise ValidationError("codigo_pais must be 2 characters")

# Schema for Error model
class ErrorSchema(SQLAlchemyAutoSchema):
    id = fields.Integer()
    transaction_id = fields.String()
    
    class Meta:
        model = Error
        load_instance = True