import uuid
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VideoRecommendationDto(BaseModel):
    id: uuid.UUID
    video_simulation_id: uuid.UUID
    document_id: uuid.UUID
    recommendations: str
    update_date: Optional[datetime]
    creation_date: datetime