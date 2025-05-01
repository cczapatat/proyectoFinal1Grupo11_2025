import json
import os
from google.cloud import pubsub_v1
from datetime import datetime
from typing import Optional
from ..models.Operations import Operation

publisher_products = pubsub_v1.PublisherClient()

class PublisherService:
    def __init__(self, project_id: Optional[str] = None, topic_id: Optional[str] = None):
        self.project_id = project_id
        self.topic_id = topic_id
     
        # Use the mocked PublisherClient in test mode
        if os.getenv('TESTING'):
            from unittest.mock import Mock
            self.publisher = Mock()
        else:
            self.publisher = pubsub_v1.PublisherClient()

    def publish_create_command(self, process_id: str, user_id: str, file_id: str, creation_time: datetime) -> bool:
     
        topic_path = self.publisher.topic_path(self.project_id, self.topic_id)

        message_dict = {
            "process_id": str(process_id),
            "user_id": user_id,
            "file_id": file_id,
            "creation_time": creation_time.isoformat(),
            "operation": Operation.CREATE.value,
            "entity" : "MANUFACTURE"
        }

        message_data = json.dumps(message_dict).encode("utf-8")

        try:
            print(f"-- Publishing message to topic {topic_path}")
            future = self.publisher.publish(topic_path, data=message_data)
           
            print(f"-- Message published: {message_dict}, future: {future.result()}")
            return True
        except Exception as e:
            print(f"Failed to publish message: {e}")
            return False