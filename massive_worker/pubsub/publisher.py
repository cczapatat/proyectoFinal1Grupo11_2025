import json
import os

from google.cloud import pubsub_v1
from ..infrastructure.entity_batch_repository import EntityBatchRepository

attemps_name_pub = os.getenv('GCP_MANUFACTURE_MASSIVE_TOPIC', 'commands_to_massive')
massive_manufacture_name_pub = os.getenv('GCP_MANUFACTURE_TOPIC', 'commands_to_manufactures')
massive_product_name_pub = os.getenv('GCP_PRODUCT_TOPIC', 'commands_to_products')
project_id = os.getenv('GCP_PROJECT_ID', 'proyectofinalmiso2025')

publisher_retry_attempt = pubsub_v1.PublisherClient()
publisher_massive_entity = pubsub_v1.PublisherClient()
topic_path_attempt = publisher_retry_attempt.topic_path(project_id, attemps_name_pub)
topic_path_massive_manufacture = publisher_massive_entity.topic_path(project_id, massive_manufacture_name_pub)
topic_path_massive_product = publisher_massive_entity.topic_path(project_id, massive_product_name_pub)

entity_batch_repository = EntityBatchRepository()

class Publisher:
    def publish_retry_attempt(self, message):
        future = publisher_retry_attempt.publish(topic_path_attempt, message.data)
        print(f"[Retry Attempt] Published: {future.result()}")

    
    def publish_massive_entity(self, entity_type, operation, process_id, file_id, user_id, json_data):
        batch_size = 100
        total_rows = len(json_data)
        current_batch = 0

        last_batch = entity_batch_repository.get_last_entity_batch(process_id)
        if last_batch:
            current_batch = last_batch.current_batch + 1

        number_of_batches = total_rows // batch_size

        for i in range(current_batch * batch_size, total_rows, batch_size):
            batch = {
                "transaction_id": process_id,
                "batch_number": current_batch,
                "operation": operation,
                "entities": json_data[i:i + batch_size],
                "entity_type": entity_type,
            }
            print(f"[Publish Massive Entity] process_id: {process_id}, batch_number: {current_batch}")

            data_str = json.dumps(batch).encode("utf-8")
            topic_path_massive_entity = topic_path_massive_manufacture

            if entity_type == "PRODUCT":
                topic_path_massive_entity = topic_path_massive_product
            
            future = publisher_massive_entity.publish(topic_path_massive_entity, data_str)
            print(f"[Massive Entity] Published: {future.result()} to topic {topic_path_massive_entity}")
            entity_batch_repository.create_entity_batch(entity_type, process_id, file_id, user_id, str(future.result()), current_batch, number_of_batches)

            current_batch += 1
    
    def get_publisher_retry_attempt(self):
        return publisher_retry_attempt