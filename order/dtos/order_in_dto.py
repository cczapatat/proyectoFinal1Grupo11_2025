import uuid
from dataclasses import dataclass, field

from ..models.enums import PAYMENT_METHOD
from .order_product_in_dto import OrderProductInDTO


@dataclass
class OrderInDTO:
    user_id: uuid = field(default=None)
    seller_id: uuid = field(default=None)
    client_id: uuid = field(default=None)
    delivery_date: str = field(default=None)
    payment_method: PAYMENT_METHOD = field(default=None)
    products: list[OrderProductInDTO] = field(default=None)
