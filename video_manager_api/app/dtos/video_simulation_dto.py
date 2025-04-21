import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class VideoSimulationDTO(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    file_path: str
    tags: str | None = None
    enabled: bool
    update_date: datetime
    creation_date: datetime