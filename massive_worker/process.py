import os
import gc
import json
import threading

from google.cloud import pubsub_v1
from .infrastructure.attempt_repository import AttemptRepository
from .infrastructure.attempt_error_repository import AttemptErrorRepository
from .services.document_manager_service import DocumentManagerService
from .pubsub.publisher import Publisher
from .models.declarative_base import session

project_id = os.getenv('GCP_PROJECT_ID', 'proyectofinalmiso2025')
attemps_subscription_id = os.getenv('GCP_MANUFACTURE_MASSIVE_SUB', 'commands_to_massive-sub')
attemps_name_pub = os.getenv('GCP_MANUFACTURE_MASSIVE_TOPIC', 'commands_to_massive')
massive_entity_name_pub = os.getenv('GCP_MANUFACTURE_TOPIC', 'commands_to_manufactures')

publisher = Publisher()
document_manager_service = DocumentManagerService()
attempt_repository = AttemptRepository()
attempt_error_repository = AttemptErrorRepository()

def log_error(context: str, process_id: str, error: Exception):
    print(f"[{context}] process_id: {process_id}, error: {str(error)}")


def process_attempts(message):
    print(f"[Process Attempts] Received: {message}")
    gc.collect()

    try:
        input_data = json.loads(message.data.decode("utf-8"))
        print(f"[Process Attempts] Input Data: {input_data}")

        operation = input_data.get("operation")
        entity = input_data.get("entity")
        process_id = input_data.get("process_id")
        file_id = input_data.get("file_id")
        user_id = input_data.get("user_id")

        if not all([operation, entity, process_id, file_id, user_id]):
            print(f"[Process Attempts] Missing required fields in input: {input_data}")
            return

        json_data = document_manager_service.get_json_from_document(file_id)
        
        if json_data is None:
            last_error = attempt_error_repository.get_last_attempt_error(process_id)
            retry_count = (last_error.retry_quantity + 1) if last_error else 1

            if retry_count <= 3:
                attempt_error_repository.create_attempt_error(operation, entity, process_id, file_id, user_id, retry_count)
                
                threading.Timer(5 * retry_count, publisher.get_publisher_retry_attempt().publish_retry_attempt, args=(message,)).start()

            message.ack()
            return

        attempt = attempt_repository.create_attempt(operation, entity, process_id, file_id, user_id)
        if not attempt:
            print("[Process Attempts] Failed to create attempt")
            return

        publisher.publish_massive_entity(entity, operation, process_id, file_id, user_id, json_data)
        print(f"[Process Attempts] Completed process_id: {process_id}")
        message.ack()

    except Exception as ex:
        log_error("Process Attempts", "", ex)
        message.nack()

    gc.collect()


if __name__ == '__main__':
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, attemps_subscription_id)

    flow_control = pubsub_v1.types.FlowControl(max_messages=10)

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=process_attempts)
    print(f"[Process Attempts] Listening on {subscription_path}...")

    with subscriber:
        try:
            streaming_pull_future.result()
        except Exception as ex:
            log_error("Main", "", ex)
            streaming_pull_future.cancel()
            streaming_pull_future.result()