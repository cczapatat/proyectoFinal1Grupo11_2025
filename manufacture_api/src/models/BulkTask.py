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
    bulk_file_url = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(256), nullable=False)
    createdAt = db.Column(DateTime, nullable=False)
    updatedAt = db.Column(DateTime, nullable=False)

class BulkTaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BulkTask
        load_instance = True
    id = fields.String()
