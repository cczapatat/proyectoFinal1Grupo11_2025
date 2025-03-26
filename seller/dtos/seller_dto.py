from dataclasses import dataclass, field

@dataclass
class SellerDTO:
    user_id: int = field(default=None)
    name: str = field(default=None)
    phone: str = field(default=None)
    email: str = field(default=None)
    zone: str = field(default=None)
    quota_expected: float = field(default=None)
    currency_quota: str = field(default=None)
    quartely_target: float = field(default=None)
    currency_target: str = field(default=None)
    performance_recomendations: str = field(default=None)
