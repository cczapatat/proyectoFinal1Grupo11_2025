from dataclasses import dataclass, field

@dataclass
class OrderDTO:
    user_id: str = field(default=None)
