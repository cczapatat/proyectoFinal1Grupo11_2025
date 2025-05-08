import uuid
from dataclasses import dataclass, field

from ..dtos.client_in_dto import ClientInDTO

from .visit_product_in_dto import VisitProductInDTO


@dataclass
class ExtendedVisitInDTO:
    visit_id: uuid = field(default=None)
    user_id: uuid = field(default=None)
    seller_id: uuid = field(default=None)
    client: ClientInDTO = field(default=None)
    description: str = field(default=None)
    visit_date: str = field(default=None)
