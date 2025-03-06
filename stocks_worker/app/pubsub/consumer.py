import os
import json
from google.cloud import pubsub_v1
from app.mappers.pubsub_mapper import map_pubsub_message_to_product_updates
from app.uow.unit_of_work import UnitOfWork
from app.repositories.stock_repository import StockRepository

GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "proyectofinalmiso2025")
STOCK_UPDATE_SUB = os.environ.get("GCP_STOCKS_SUB", "commands_to_stock-sub")

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(GCP_PROJECT_ID, STOCK_UPDATE_SUB)

def callback(message):
    try:
        print(" === Inicia actualizacion de stocks ====" )
        payload_str = message.data.decode("utf-8")
        print(f" > Mensaje recibido: {payload_str}")
        payload = json.loads(payload_str)
        # Mapear el mensaje a una lista de ProductUpdateDTO
        product_updates = map_pubsub_message_to_product_updates(payload)
        with UnitOfWork() as uow:
            repo = StockRepository(uow.session)
            results = repo.update_stocks(product_updates)
            print(" === Actualización de stocks completada ====" )
        message.ack()
    except Exception as e:
        print(f"Error al procesar mensaje: {e}")
        message.nack()

def consume_messages():
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Escuchando mensajes en {subscription_path}...")
    try:
        streaming_pull_future.result()
    except Exception as e:
        print(f"Excepción en el suscriptor: {e}")
        streaming_pull_future.cancel()