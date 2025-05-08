import uuid
from dataclasses import dataclass, field


@dataclass
class ClientInDTO:
    id: uuid = field(default=None)
    name: str = field(default=None)
    client_type: str = field(default=None)
    zone: str = field(default=None)