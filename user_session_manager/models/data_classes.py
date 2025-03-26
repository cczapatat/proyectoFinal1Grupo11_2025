from dataclasses import dataclass

@dataclass
class LoginIn:
    id: int
    id_usuario: int = 0
    type: str = 'SELLER'