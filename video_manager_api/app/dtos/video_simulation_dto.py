import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class VideoSimulationDTO(BaseModel):
    id: uuid.UUID | None = None
    document_id: uuid.UUID
    file_path: str
    tags: str | None = None
    enabled: bool
    update_date: datetime | None = None
    creation_date: datetime | None = None

    class Config:
        allow_population_by_field_name = True
