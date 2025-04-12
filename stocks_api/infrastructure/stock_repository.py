import uuid

from sqlalchemy import asc

from ..config.db import db
from ..dtos.store_x_products_dto import ProductStockDTO, StoreXProductsDTO
from ..models.stock_model import Stock


class StockRepository:
    @staticmethod
    def get_documents(page: int = 1, per_page: int = 10) -> list[Stock]:
        offset = (page - 1) * per_page
        stocks = db.session.query(Stock).filter(Stock.quantity_in_stock > 0).order_by(
            asc(Stock.creation_date)).offset(
            offset).limit(per_page).all()

        return stocks

    @staticmethod
    def get_total_documents() -> int:
        total = db.session.query(Stock).filter(Stock.quantity_in_stock > 0).count()

        return total

    @staticmethod
    def get_documents_by_ids(ids: list[uuid.uuid4]) -> list[Stock]:
        stocks = db.session.query(Stock).filter(Stock.id.in_(ids)).all()

        return stocks

    @staticmethod
    def get_stocks_by_store_id(id_store: uuid.uuid4) -> list[StoreXProductsDTO]:
        stocks = db.session.query(Stock).filter_by(id_store=id_store).all()
        store_x_products_dto = StoreXProductsDTO(id_store=id_store, stocks=[])
        for stock in stocks:
            product_stock_dto = ProductStockDTO(
                id=stock.id,
                id_product=stock.id_product,
                assigned_stock=stock.quantity_in_stock
            )
            store_x_products_dto.stocks.append(product_stock_dto)

        return store_x_products_dto

    @staticmethod
    def assign_stock_to_store(id: uuid.uuid4, store_id: uuid.uuid4, product_id: uuid.uuid4, assigned_stock: int):
        # Check if the Stock entry already exists
        if id is None or id == '':
            # Create a new Stock entry if it doesn't exist
            stock = Stock(id=uuid.uuid4(), id_product=product_id, id_store=store_id, quantity_in_stock=assigned_stock)
            db.session.add(stock)
        else:
            # Update the existing Stock entry
            stock = db.session.query(Stock).filter_by(id=id).first()
            if stock is not None:
                stock.id_product = product_id
                stock.id_store = store_id
                stock.last_quantity = stock.quantity_in_stock
                stock.quantity_in_stock = assigned_stock
    # Commit the changes to the database
        db.session.commit()

    @staticmethod
    def unassign_stock_to_store(id_store: uuid.uuid4, selected_stocks: list[ProductStockDTO]):
        # get all the stocks by store id
        stocks = db.session.query(Stock).filter_by(id_store=id_store).all()
        # if any of the stocks are not in the selected stocks, remove them
        for stock in stocks:
            if stock.id_product not in [selected_stock.id_product for selected_stock in selected_stocks]:
                db.session.delete(stock)
        # commit the changes to the database
        db.session.commit()
        # return the stocks left
        stocks = db.session.query(Stock).filter_by(id_store=id_store).all()
        return stocks
