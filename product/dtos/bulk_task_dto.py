from dataclasses import dataclass, field
import uuid

@dataclass
class BulkTaskDTO:
    user_id: uuid = field(default=None)
    file_id: uuid = field(default=None)
    status: str = field(default=None)
