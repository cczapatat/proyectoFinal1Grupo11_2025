import uuid

from ..dtos.store_in_dto import StoreInDTO
from ..infrastructure.store_repository import StoreRepository

store_repository = StoreRepository()


class StoreManager:
    @staticmethod
    def get_store_by_id(id_store: uuid.uuid4) -> dict | None:
        store = store_repository.get_store_by_id(id_store)

        if store is None:
            return None

        return store.to_dict()

    @staticmethod
    def create_store(store_in_dto: StoreInDTO) -> dict:
        store = store_repository.create_store(store_in_dto)

        return store.to_dict()

    @staticmethod
    def get_stores_paginate(page: int = 1, per_page: int = 10) -> list[dict]:
        stores = store_repository.get_stores_by_page(page=page, per_page=per_page)
        print('ooooooo')
        return [store.to_dict() for store in stores]
