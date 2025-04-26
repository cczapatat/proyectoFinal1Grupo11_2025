import os
import gc
import json

from google.cloud import pubsub_v1

from products_worker.models.Operations import BULK_STATUS

from .infrastructure.bulk_task_repository import BulkTaskRepository
from .infrastructure.product_repository import ProductRepository
from .dtos.product_dto import ProductDTO

project_id = os.getenv('GCP_PROJECT_ID', 'proyectofinalmiso2025')
massive_entity_subscription_id = os.getenv('GCP_PRODUCT_MASSIVE_SUB', 'commands_to_products-sub')

product_repository = ProductRepository()
bulk_task_repository = BulkTaskRepository()

def log_error(context: str, process_id: str, error: Exception):
    print(f"[{context}] process_id: {process_id}, error: {str(error)}")

def process_create_product( transaction_id: str, entities):
    products_dto = []
    for index, product_data in enumerate(entities):
        print(f"[Process Create Product] Entity: {product_data}")

        product_data = {key.lstrip('\ufeff'): value for key, value in product_data.items()}

        product_dto = ProductDTO(
            manufacturer_id=product_data.get("manufacturer_id"),
            name=product_data.get("name"),
            description=product_data.get("description"),
            category=product_data.get("category"),
            unit_price=product_data.get("unit_price"),
            currency_price=product_data.get("currency_price"),
            is_promotion=product_data.get("is_promotion"),
            discount_price=product_data.get("discount_price"),
            expired_at=product_data.get("expired_at"),
            url_photo=product_data.get("url_photo"),
            store_conditions=product_data.get("store_conditions")
        )
        products_dto.append(product_dto)
    
    try:
        status = BULK_STATUS.BUlK_FAILED
        products = product_repository.create_massive_products(transaction_id, products_dto)
        print(f"[Process Create Product] Products created. quantity: {len(products)}")

        if (len(products) > 0):
            status = BULK_STATUS.BULK_COMPLETED
        
        bulk_task_repository.update_bulk_task_status(transaction_id, status)
            
    except Exception as ex:
        log_error("Process Create Product", transaction_id, ex)
        print(f"[Process Create Product] Error: {str(ex)}")
    finally:
        del products_dto
        gc.collect()


def process_products(message):
    print(f"[Process Products] Received: {message}")

    try:
        input_data = json.loads(message.data.decode("utf-8"))

        entity_type = input_data.get("entity_type")

        if entity_type == "PRODUCT":
            transaction_id = input_data.get("transaction_id")
            operation = input_data.get("operation")
            entities = input_data.get("entities")

            if operation == "CREATE":
                process_create_product(transaction_id, entities)
                
        message.ack()

    except Exception as ex:
        log_error("Process Products", "", ex)
        message.ack()




if __name__ == '__main__':
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, massive_entity_subscription_id)

    flow_control = pubsub_v1.types.FlowControl(max_messages=10)

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=process_products)
    print(f"[Process Products] Listening on {subscription_path}...")

    with subscriber:
        try:
            streaming_pull_future.result()
        except Exception as ex:
            log_error("Main", "", ex)
            streaming_pull_future.cancel()
            streaming_pull_future.result()