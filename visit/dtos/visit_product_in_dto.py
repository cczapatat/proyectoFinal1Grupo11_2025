from dataclasses import dataclass, field


@dataclass
class VisitProductInDTO:
    product_id: str = field(default=None),
