from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.models.stock import Stock
from app.models.update_stock_attempt import UpdateStockAttempt, UpdateStatus
from app.dtos.product_update_dto import ProductUpdateDTO
from threading import Thread
from app.pubsub.dispatcher import dispatch_stock_updated_event

class StockRepository:
    def __init__(self, session: Session):
        self.session = session

    def update_stocks(self, product_updates: List[ProductUpdateDTO]) -> List:
        results = []
        for update_dto in product_updates:
            product_id = update_dto.product_id
            requested_units = update_dto.units

            update_attempt = UpdateStockAttempt(
                status=UpdateStatus.RECEIVED,
                creation_date=datetime.utcnow(),
                last_update_date=datetime.utcnow()
            )
            self.session.add(update_attempt)
            try:
                with self.session.begin_nested():
                    stock = self.session.query(Stock).filter(Stock.id == product_id).first()
                    if not stock:
                        update_attempt.status = UpdateStatus.ROLLED_BACK
                        update_attempt.last_update_date = datetime.utcnow()
                        results.append({"product_id": str(product_id), "error": "Producto no encontrado"})
                        continue

                    if stock.quantity_in_stock < requested_units:
                        update_attempt.status = UpdateStatus.ROLLED_BACK
                        update_attempt.last_update_date = datetime.utcnow()
                        results.append({"product_id": str(product_id), "error": "Stock insuficiente"})
                        continue

                    stock.last_quantity = stock.quantity_in_stock
                    stock.quantity_in_stock -= requested_units
                    stock.update_date = datetime.utcnow()

                    update_attempt.status = UpdateStatus.COMMITTED
                    update_attempt.last_update_date = datetime.utcnow()

                    result = {
                        "product_id": str(stock.id),
                        "product_name": stock.product_name,
                        "last_quantity": stock.last_quantity,
                        "new_quantity": stock.quantity_in_stock,
                        "status": update_attempt.status.value
                    }
                    results.append(result)

                    # Lanzar un hilo para publicar el evento
                    thread = Thread(
                        target=dispatch_stock_updated_event,
                        args=(result["product_id"], result["product_name"], result["last_quantity"], result["new_quantity"]),
                        daemon=True
                    )
                    thread.start()
            except Exception as e:
                self.session.rollback()
                update_attempt.status = UpdateStatus.FAILED
                update_attempt.last_update_date = datetime.utcnow()
                self.session.add(update_attempt)
                self.session.commit()
                results.append({"product_id": str(product_id), "error": str(e)})
        self.session.commit()
        return results