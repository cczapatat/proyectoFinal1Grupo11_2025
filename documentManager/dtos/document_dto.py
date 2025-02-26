from dataclasses import dataclass, field

@dataclass
class DocumentDTO:
    user_id: str = field(default=None)
    file_name: str = field(default=None)
    path_source: str = field(default=None)