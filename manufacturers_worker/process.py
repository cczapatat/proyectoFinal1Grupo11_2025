import os
import gc
import json
from google.cloud import pubsub_v1
from .models.Operations import BULK_STATUS
from .infrastructure.bulk_task_repository import BulkTaskRepository
from .infrastructure.manufacturer_repository import ManufacturerRepository
from .dtos.manufacturer_dto import ManufacturerDTO

project_id = os.getenv('GCP_PROJECT_ID', 'proyectofinalmiso2025')
massive_entity_subscription_id = os.getenv('GCP_PRODUCT_MASSIVE_SUB', 'commands_to_manufactures-sub')

manufacturer_repository = ManufacturerRepository()
bulk_task_repository = BulkTaskRepository()

def log_error(context: str, process_id: str, error: Exception):
    print(f"[{context}] process_id: {process_id}, error: {str(error)}")

def parse_manufacturer_data(manufacturer_data):
    manufacturer_data = {key.lstrip('\ufeff'): value for key, value in manufacturer_data.items()}
    return ManufacturerDTO(
        name=manufacturer_data.get("name"),
        address=manufacturer_data.get("address"),
        phone=manufacturer_data.get("phone"),
        email=manufacturer_data.get("email"),
        country=manufacturer_data.get("country"),
        tax_conditions=manufacturer_data.get("tax_conditions"),
        legal_conditions=manufacturer_data.get("legal_conditions"),
        rating_quality=manufacturer_data.get("rating_quality")
    )

def filter_existing_manufacturers(manufacturers_dto, existing_emails, existing_phones):
    filtered_manufacturers = []
    for manufacturer_dto in manufacturers_dto:
        if manufacturer_dto.email in existing_emails or manufacturer_dto.phone in existing_phones:
            print(f"[Warning] Manufacturer already exists: email={manufacturer_dto.email}, phone={manufacturer_dto.phone}")
        else:
            filtered_manufacturers.append(manufacturer_dto)
    return filtered_manufacturers

def process_create_manufacturer(transaction_id: str, entities):
    try:
        manufacturers_dto = [parse_manufacturer_data(data) for data in entities]
        emails = [dto.email for dto in manufacturers_dto]
        phones = [dto.phone for dto in manufacturers_dto]

        existing_manufacturers = manufacturer_repository.get_existing_manufacturers_by_email_or_phone(emails, phones)
        existing_emails = {manufacturer.email for manufacturer in existing_manufacturers}
        existing_phones = {manufacturer.phone for manufacturer in existing_manufacturers}

        filtered_manufacturers_dto = filter_existing_manufacturers(manufacturers_dto, existing_emails, existing_phones)

        status = BULK_STATUS.BUlK_FAILED
        if filtered_manufacturers_dto:
            manufacturers = manufacturer_repository.create_massive_manufacturers(transaction_id, filtered_manufacturers_dto)
            print(f"[Process Create Manufacturers] Manufacturers created. Quantity: {len(manufacturers)}")
            if manufacturers:
                status = BULK_STATUS.BULK_COMPLETED

        bulk_task_repository.update_bulk_task_status(transaction_id, status)

    except Exception as ex:
        log_error("Process Create Manufacturer", transaction_id, ex)
    finally:
        del manufacturers_dto
        gc.collect()

def process_manufacturers(message):
    print(f"[Process Manufacturers] Received: {message}")

    try:
        input_data = json.loads(message.data.decode("utf-8"))
        entity_type = input_data.get("entity_type")

        if entity_type == "MANUFACTURE":
            transaction_id = input_data.get("transaction_id")
            operation = input_data.get("operation")
            entities = input_data.get("entities")

            if operation == "CREATE":
                process_create_manufacturer(transaction_id, entities)

        message.ack()

    except Exception as ex:
        log_error("Process Manufacturers", "", ex)
        message.ack()

if __name__ == '__main__':
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, massive_entity_subscription_id)

    flow_control = pubsub_v1.types.FlowControl(max_messages=10)

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=process_manufacturers)
    print(f"[Process Manufacturers] Listening on {subscription_path}...")

    with subscriber:
        try:
            streaming_pull_future.result()
        except Exception as ex:
            log_error("Main", "", ex)
            streaming_pull_future.cancel()
            streaming_pull_future.result()