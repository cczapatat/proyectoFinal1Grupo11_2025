from dataclasses import dataclass, field


@dataclass
class OrderProductInDTO:
    product_id: str = field(default=None),
    units: int = field(default=None)
