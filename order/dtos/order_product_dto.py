from dataclasses import dataclass, field

@dataclass
class OrderProductDTO:
    order_id: str = field(default=None),
    product_id: str = field(default=None),
    units: int = field(default=None)
