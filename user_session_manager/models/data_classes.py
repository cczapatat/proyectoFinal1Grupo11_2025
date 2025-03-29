from dataclasses import dataclass


@dataclass
class LoginIn:
    id: str
    id_user: int = 0
    type: str = 'SELLER'

    def to_serializable(self):
        return {
            'id': self.id,
            'id_user': self.id_user,
            'type': self.type
        }.__str__()
