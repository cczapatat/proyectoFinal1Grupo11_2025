from dataclasses import dataclass, field

@dataclass
class ProductDTO:
    manufacturer_id: str = field(default=None)
    name: str = field(default=None)
    description: str = field(default=None)
    category: str = field(default=None)
    unit_price: float = field(default=None)
    currency_price: str = field(default=None)
    is_promotion: bool = field(default=None)
    discount_price: float = field(default=None)
    expired_at: str = field(default=None)
    url_photo: str = field(default=None)
    store_conditions: str = field(default=None)
