from sqlalchemy import asc

from ..config.db import db
from ..models.stock_model import Stock


class StockRepository:
    @staticmethod
    def get_documents(page: int = 1, per_page: int = 10) -> list[Stock]:
        offset = (page - 1) * per_page
        documents = db.session.query(Stock).order_by(asc(Stock.product_name)).offset(offset).limit(per_page).all()

        return documents
