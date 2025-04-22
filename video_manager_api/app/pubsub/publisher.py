import os
import json
import logging
from google.cloud import pubsub_v1

# Configuración
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "proyectofinalmiso2025")
VIDEO_SIMULATION_TOPIC = os.environ.get("GCP_VIDEO_SIMULATION_TOPIC", "commands_to_video_recommendations")

# Bandera para verificar si el publicador de Pub/Sub está disponible
pubsub_publisher_available = False
publisher_client = None

try:
    publisher_client = pubsub_v1.PublisherClient()
    pubsub_publisher_available = True
except Exception as e:
    logging.warning(f"Inicialización del publicador PubSub fallida: {e}. Ejecutando en modo de desarrollo sin publicación en PubSub.")

def dispatch_video_simulation_event(video_id: str, document_id: str, file_path: str, enabled: bool, tags: str | None = None) -> bool:
    """
    Envía un evento de simulación de video al tema de Pub/Sub.
    
    Args:
        video_id: Identificador único para el video
        document_id: Identificador del documento asociado con el video
        file_path: Ruta al archivo de video
        enabled: Si el video está habilitado
        tags: Etiquetas opcionales asociadas con el video
        
    Returns:
        bool: True si el envío fue exitoso, False en caso contrario
    """
    if not pubsub_publisher_available:
        logging.info(f"Omitiendo envío de evento de simulación de video para el video {video_id} (PubSub no disponible)")
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
        print(f"Publicando evento de simulación de video para el video {video_id}...")
        future = publisher_client.publish(topic_path, data=message_data)
        future.result()
        print(f"Evento de simulación de video para el video {video_id} publicado exitosamente.")
        return True
    except Exception as e:
        print(f"Error al publicar el evento: {e}")
        return False

