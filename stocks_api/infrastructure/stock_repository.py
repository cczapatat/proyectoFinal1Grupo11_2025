import uuid

from sqlalchemy import asc

from ..config.db import db
from ..models.stock_model import Stock, StoreXStock


class StockRepository:
    @staticmethod
    def get_documents(page: int = 1, per_page: int = 10) -> list[Stock]:
        offset = (page - 1) * per_page
        stocks = db.session.query(Stock).order_by(asc(Stock.product_name)).offset(offset).limit(per_page).all()

        return stocks

    @staticmethod
    def get_documents_by_ids(ids: list[uuid.uuid4]) -> list[Stock]:
        stocks = db.session.query(Stock).filter(Stock.id.in_(ids)).all()

        return stocks

    @staticmethod
    def get_stocks_ids_by_store_id(id_store: uuid.uuid4) -> list[int]:
        stocks_ids = db.session.query(StoreXStock).filter_by(store_id=id_store).all()

        return stocks_ids
