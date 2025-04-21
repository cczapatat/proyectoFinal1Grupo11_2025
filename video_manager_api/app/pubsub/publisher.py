import os
import json
import logging
from google.cloud import pubsub_v1

# Configuration
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "proyectofinalmiso2025")
VIDEO_SIMULATION_TOPIC = os.environ.get("GCP_VIDEO_SIMULATION_TOPIC", "video_to_simulation")

# Flag to track if Pub/Sub publisher is available
pubsub_publisher_available = False
publisher_client = None

try:
    publisher_client = pubsub_v1.PublisherClient()
    pubsub_publisher_available = True
except Exception as e:
    logging.warning(f"PubSub publisher initialization failed: {e}. Running in development mode without PubSub publishing.")

def dispatch_video_simulation_event(video_id: str, document_id: str, file_path: str, enabled: bool, tags: str | None = None) -> bool:
    """
    Dispatches a video simulation event to the Pub/Sub topic.
    
    Args:
        video_id: Unique identifier for the video
        document_id: Document identifier associated with the video
        file_path: Path to the video file
        enabled: Whether the video is enabled
        tags: Optional tags associated with the video
        
    Returns:
        bool: True if dispatch was successful, False otherwise
    """
    if not pubsub_publisher_available:
        logging.info(f"Skipping video simulation event dispatch for video {video_id} (PubSub not available)")
        return False
        
    topic_path = publisher_client.topic_path(GCP_PROJECT_ID, VIDEO_SIMULATION_TOPIC)
    message_dict = {
        "video_id": video_id,
        "document_id": document_id,
        "file_path": file_path,
        "tags": tags,
        "enabled": enabled,
    }
    message_data = json.dumps(message_dict).encode("utf-8")
    try:
        print(f"Publicando evento de simulación de video para video {video_id}...")
        future = publisher_client.publish(topic_path, data=message_data)
        future.result()
        return True
    except Exception as e:
        print(f"Error al publicar el evento: {e}")
        return False

