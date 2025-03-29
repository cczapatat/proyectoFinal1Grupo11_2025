from dataclasses import dataclass, field

@dataclass
class ClientDTO:
    user_id: int = field(default=None)
    seller_id: str = field(default=None)
    name: str = field(default=None)
    phone: str = field(default=None)
    email: str = field(default=None)
    address: str = field(default=None)
    client_type: str = field(default=None)
    zone: str = field(default=None)
    