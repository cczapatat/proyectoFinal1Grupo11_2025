import uuid
import datetime
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import Base

class VideoRecommendation(Base):
    __tablename__ = "video_recommendations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    video_simulation_id = Column(UUID(as_uuid=True), nullable=False)
    document_id = Column(UUID(as_uuid=True), nullable=False)
    recommendations = Column(String, nullable=False)
    update_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "video_simulation_id": str(self.video_simulation_id),
            "document_id": str(self.document_id),
            "recommendations": self.recommendations,
            "update_date": self.update_date.isoformat() if self.update_date else None,
            "creation_date": self.creation_date.isoformat() if self.creation_date else None,
        }

