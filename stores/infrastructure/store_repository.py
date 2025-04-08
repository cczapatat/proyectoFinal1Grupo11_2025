import uuid
from datetime import datetime

from ..config.db import db
from ..dtos.store_in_dto import StoreInDTO
from ..models.store_model import Store


class StoreRepository:
    @staticmethod
    def get_store_by_id(id_store: uuid.uuid4) -> Store | None:
        store = db.session.query(Store).filter_by(id=id_store).one_or_none()

        return store

    @staticmethod
    def create_store(store_in_dto: StoreInDTO) -> Store:
        store = Store()
        store.name = store_in_dto.name
        store.phone = store_in_dto.phone
        store.email = store_in_dto.email
        store.address = store_in_dto.address
        store.capacity = store_in_dto.capacity
        store.state = store_in_dto.state
        store.security_level = store_in_dto.security_level
        store.created_at = datetime.now()
        store.updated_at = datetime.now()

        db.session.add(store)
        db.session.commit()

        return store

    @staticmethod
    def get_stores_by_page(page: int, per_page: int) -> list[Store]: 
        offset = (page - 1) * per_page
        stores = db.session.query(Store).order_by(Store.name).offset(offset).limit(per_page).all()

        return stores
