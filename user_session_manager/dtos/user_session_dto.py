from dataclasses import dataclass, field

@dataclass
class UserSessionDTO:
    email: str = field(default=None)
    password: str = field(default=None)
    type: str = field(default=None)
