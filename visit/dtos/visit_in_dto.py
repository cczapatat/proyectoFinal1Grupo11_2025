import uuid
from dataclasses import dataclass, field

from .visit_product_in_dto import VisitProductInDTO


@dataclass
class VisitInDTO:
    user_id: uuid = field(default=None)
    seller_id: uuid = field(default=None)
    client_id: uuid = field(default=None)
    description: str = field(default=None)
    visit_date: str = field(default=None)
    products: list[VisitProductInDTO] = field(default=None)
