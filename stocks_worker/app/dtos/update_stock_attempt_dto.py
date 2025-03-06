import uuid
from pydantic import BaseModel

class UpdateAttemptDTO(BaseModel):
    id: uuid.UUID
    requested_stock: int