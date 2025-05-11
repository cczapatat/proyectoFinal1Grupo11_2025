import json
import os
import uuid
from datetime import datetime
from threading import Thread
from typing import List

from app.cache.redis_handler import update_stock_cache
from app.dtos.product_update_dto import ProductUpdateDTO
from app.models.stock import Stock
from app.models.update_stock_attempt import UpdateStockAttempt, UpdateStatus
from google.cloud import pubsub_v1
from sqlalchemy.orm import Session

project_id = os.environ.get('GCP_PROJECT_ID', 'proyectofinalmiso2025')
commands_to_stock_update_name_pub = os.environ.get('GCP_STOCK_UPDATE_TOPIC', 'commands_to_stock_update')


def _get_publisher():
    if str(os.getenv('TESTING')).lower() == 'true':
        return publisher_stock_update
    return pubsub_v1.PublisherClient()


publisher_stock_update = pubsub_v1.PublisherClient()
topic_path_stock_update = publisher_stock_update.topic_path(project_id, commands_to_stock_update_name_pub)


def _publish_update_stock(stock_id: uuid, product_base_id: uuid, stock_unit: int) -> None:
    data = {"stock_id": str(stock_id), "product_id": str(product_base_id), "stock_unit": stock_unit}
    data_str = json.dumps(data).encode("utf-8")
    future = _get_publisher().publish(topic_path_stock_update, data_str)
    print(f"[Publish Update Stock] Published: {future.result()}, data: {data_str}")


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
                last_update_date=datetime.utcnow(),
                product_id=product_id
            )
            self.session.add(update_attempt)
            print(f"Actualizando stock para producto {product_id}...")

            try:
                with self.session.begin_nested():
                    # Validar existencia del producto
                    stock = self.session.query(Stock).filter(Stock.id == product_id).first()
                    if not stock:
                        update_attempt.status = UpdateStatus.ROLLED_BACK
                        update_attempt.last_update_date = datetime.utcnow()
                        print(f" > Producto {product_id} no encontrado")
                        results.append({"product_id": str(product_id), "error": "Producto no encontrado"})
                        continue
                    # Validar stock suficiente
                    if stock.quantity_in_stock < requested_units:
                        update_attempt.status = UpdateStatus.ROLLED_BACK
                        update_attempt.last_update_date = datetime.utcnow()
                        print(f" > Stock insuficiente para producto {product_id}")
                        results.append({"product_id": str(product_id), "error": "Stock insuficiente"})
                        continue

                    # Guardamos el stock anterior para la validación.
                    stock.last_quantity = stock.quantity_in_stock
                    stock.quantity_in_stock -= requested_units
                    stock.update_date = datetime.utcnow()

                    update_attempt.status = UpdateStatus.COMMITTED
                    update_attempt.last_update_date = datetime.utcnow()

                    print(
                        f" > Stock actualizado para producto {product_id}, unidades restantes: {stock.quantity_in_stock}, unidades solicitadas: {requested_units}")
                # Hacer flush para obtener el ID del intento de actualización
                self.session.flush()

                # Reconsultar el registro actualizado para validar
                updated_stock = self.session.query(Stock).filter(Stock.id == product_id).first()
                expected_quantity = stock.last_quantity - requested_units
                # Validar que el stock se haya actualizado correctamente
                if not updated_stock or updated_stock.quantity_in_stock != expected_quantity:
                    update_attempt.status = UpdateStatus.FAILED
                    update_attempt.last_update_date = datetime.utcnow()
                    self.session.flush()
                    print(f" > Validación fallida para producto {product_id}")
                    results.append({"product_id": str(product_id), "error": "Validación fallida en la actualización"})
                    continue

                result = {
                    "product_id": str(updated_stock.id),
                    "last_quantity": stock.last_quantity,
                    "new_quantity": updated_stock.quantity_in_stock,
                    "status": update_attempt.status.value
                }
                results.append(result)

                # Actualizar Redis y despachar evento solo después de validación exitosa.
                thread_redis = Thread(
                    target=update_stock_cache,
                    args=(result["product_id"], result["new_quantity"]),
                    daemon=True
                )
                thread_redis.start()

                # Despachar evento de stock actualizado
                _publish_update_stock(updated_stock.id, updated_stock.id_product, updated_stock.quantity_in_stock)

            except Exception as e:
                print(f" > Error al actualizar stock para producto {product_id}: {e}")
                self.session.rollback()
                update_attempt.status = UpdateStatus.FAILED
                update_attempt.last_update_date = datetime.utcnow()
                self.session.add(update_attempt)
                self.session.commit()
                results.append({"product_id": str(product_id), "error": str(e)})
        self.session.commit()
        return results
