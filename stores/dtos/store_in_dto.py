from dataclasses import dataclass, field

from ..models.enums import STATE, SECURITY_LEVEL


@dataclass
class StoreInDTO:
    name: str = field(default=None)
    phone: str = field(default=None)
    email: str = field(default=None)
    address: str = field(default=None)
    capacity: int = field(default=None)
    state: STATE = field(default=None)
    security_level: SECURITY_LEVEL = field(default=None)
