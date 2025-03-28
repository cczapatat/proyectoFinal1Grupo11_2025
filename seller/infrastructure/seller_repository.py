from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from ..models.seller_model import Seller

class SellerRepository:
    def __init__(self, session: Session):
        self._session = session

    def create_seller(self, seller_data: dict) -> Seller:
        # Convert string UUIDs to UUID objects
        seller_data['id'] = uuid4()
        if isinstance(seller_data.get('user_id'), str):
            seller_data['user_id'] = UUID(seller_data['user_id'])

        seller = Seller(**seller_data)
        self._session.add(seller)
        self._session.flush()
        return seller

    def get_seller_by_user_id(self, user_id) -> Seller:
        if isinstance(user_id, UUID):
            user_id = str(user_id)
        user_id_uuid = UUID(user_id)
        return self._session.query(Seller).filter(Seller.user_id == user_id_uuid).first()
