from dataclasses import dataclass, field

@dataclass
class ManufacturerDTO:
    name: str = field(default=None)
    address: str = field(default=None)
    phone: str = field(default=None)
    email: str = field(default=None)
    country: str = field(default=None)
    tax_conditions: str = field(default=None)
    legal_conditions: str = field(default=None)
    rating_quality: str = field(default=None)
    created_at: str = field(default=None)
    updated_at: str = field(default=None)