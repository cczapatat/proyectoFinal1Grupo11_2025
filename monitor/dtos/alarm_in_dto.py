import uuid
from dataclasses import dataclass, field


@dataclass
class AlarmInDTO:
    user_id: uuid = field(default=None)
    manufacture_id: uuid = field(default=None)
    product_id: uuid = field(default=None)
    minimum_value: int | None = field(default=None)
    maximum_value: int | None = field(default=None)
    notes: str = field(default=None)
