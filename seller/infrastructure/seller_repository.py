import uuid
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

    def get_seller_by_id(self, seller_id: uuid.uuid4) -> Seller | None:
        return self._session.query(Seller).filter_by(id=seller_id).one_or_none()

    def get_seller_by_user_id(self, user_id: uuid.uuid4) -> Seller | None:
        return self._session.query(Seller).filter_by(user_id=user_id).one_or_none()

    def get_all_sellers(self) -> list[Seller]:
        return self._session.query(Seller).all()
