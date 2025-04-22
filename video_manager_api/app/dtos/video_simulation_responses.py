from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

class VideoSimulationResponse(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    file_path: str
    tags: Optional[str] = None
    enabled: bool
    update_date: datetime
    creation_date: datetime

    class Config:
        orm_mode = True

class VideoSimulationListResponse(BaseModel):
    mensaje: str
    cantidad: int
    videos: List[VideoSimulationResponse]

class VideoSimulationCreateResponse(BaseModel):
    mensaje: str
    resultado: VideoSimulationResponse