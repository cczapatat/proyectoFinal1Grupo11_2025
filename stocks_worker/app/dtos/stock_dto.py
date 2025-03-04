import uuid
from datetime import datetime
from pydantic import BaseModel

class StockDTO(BaseModel):
    id: uuid.UUID
    product_name: str
    quantity_in_stock: int
    last_quantity: int
    enabled: bool
    update_date: datetime
    creation_date: datetime