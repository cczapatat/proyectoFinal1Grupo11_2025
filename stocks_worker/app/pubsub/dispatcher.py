import os
import json
from google.cloud import pubsub_v1

GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "proyectofinalmiso2025")
STOCK_UPDATE_TOPIC = os.environ.get("GCP_STOCKS_TOPIC", "commands_to_stock")

publisher_client = pubsub_v1.PublisherClient()

def dispatch_stock_updated_event(stock_id: str, product_name: str, last_quantity: int, new_quantity: int) -> bool:
    topic_path = publisher_client.topic_path(GCP_PROJECT_ID, STOCK_UPDATE_TOPIC)
    message_dict = {
        "id": stock_id,
        "product_name": product_name,
        "last_quantity": last_quantity,
        "new_quantity": new_quantity
    }
    message_data = json.dumps(message_dict).encode("utf-8")
    try:
        print(f"Publicando evento de stock actualizado para producto {stock_id}...")
        future = publisher_client.publish(topic_path, data=message_data)
        future.result()
        return True
    except Exception as e:
        print(f"Error al publicar el evento: {e}")
        return False