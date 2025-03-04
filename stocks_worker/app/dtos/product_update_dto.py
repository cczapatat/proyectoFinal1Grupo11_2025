import uuid
from pydantic import BaseModel

class ProductUpdateDTO(BaseModel):
    product_id: uuid.UUID
    units: int