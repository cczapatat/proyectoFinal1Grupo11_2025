import uuid

from ..dtos.store_in_dto import StoreInDTO
from ..infrastructure.store_repository import StockRepository

stock_repository = StockRepository()


class StoreManager:
    @staticmethod
    def get_store_by_id(id_store: uuid.uuid4) -> dict | None:
        store = stock_repository.get_store_by_id(id_store)

        if store is None:
            return None

        return store.to_dict()

    @staticmethod
    def create_store(store_in_dto: StoreInDTO) -> dict:
        store = stock_repository.create_store(store_in_dto)

        return store.to_dict()
