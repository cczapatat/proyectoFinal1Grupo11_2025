import os
import json
import logging
import asyncio
from typing import Dict, Any
from google.cloud import pubsub_v1
from app.repositories.video_recommendation_repository import VideoRecommendationRepository
from app.core.db import SessionLocal

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Configuración
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "proyectofinalmiso2025")
VIDEO_SIMULATION_SUB = os.environ.get("GCP_VIDEO_SIMULATION_SUB", "commands_to_video_recommendations_sub")

# Inicializar cliente con manejo de errores
pubsub_available = False
subscriber = None
subscription_path = None

try:
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(GCP_PROJECT_ID, VIDEO_SIMULATION_SUB)
    pubsub_available = True
    logging.info(f"PubSub inicializado con suscripción: {subscription_path}")
except Exception as e:
    logging.warning(f"Inicialización de PubSub fallida: {e}. Ejecutando en modo de desarrollo sin PubSub.")

async def process_message(message_data: Dict[str, Any]) -> None:
    """
    Procesa el mensaje y genera recomendaciones
    
    Args:
        message_data: Diccionario que contiene los datos del mensaje
    """
    video_id = message_data.get("video_id")
    document_id = message_data.get("document_id")
    tags = message_data.get("tags")
    
    if not video_id or not document_id:
        logging.error(f"Formato de mensaje inválido: {message_data}")
        return
    
    logging.info(f"Procesando recomendación para el video {video_id} con etiquetas: {tags}")
    
    try:
        # Crear sesión de BD
        session = SessionLocal()
        try:
            # Procesar recomendación
            repo = VideoRecommendationRepository(session)
            print(f"Se van a procesar los tags: {tags}")
            await repo.create_recommendation(video_id, document_id, tags)
            logging.info(f"Recomendación creada exitosamente para el video {video_id}")
        finally:
            session.close()
    except Exception as e:
        logging.error(f"Error al procesar la recomendación: {e}")

def callback(message):
    """
    Función de callback para el procesamiento de mensajes PubSub
    
    Args:
        message: Mensaje de PubSub
    """
    try:
        logging.info(f"Mensaje recibido: {message.data}")
        payload = json.loads(message.data.decode("utf-8"))
        
        # Usar asyncio para procesar funciones asíncronas
        asyncio.run(process_message(payload))
        
        # Confirmar mensaje
        message.ack()
        logging.info("Mensaje confirmado")
    except Exception as e:
        logging.error(f"Error al procesar el mensaje: {e}")
        # Confirmar para prevenir reentrega, pero registrar el error
        message.ack()
def consume_messages():
    """Comienza a consumir mensajes de PubSub"""
    if not pubsub_available:
        logging.info("PubSub no disponible. Ejecutando en modo de desarrollo.")
        return
    
    logging.info(f"Iniciando suscriptor en {subscription_path}")
    
    # Inicializar el suscriptor con streaming pull
    streaming_pull_future = subscriber.subscribe(
        subscription_path, 
        callback=callback,
        flow_control=pubsub_v1.types.FlowControl(max_messages=10)
    )
    
    try:
        # Evitar que el hilo principal se cierre
        logging.info("Escuchando mensajes. Presione Ctrl+C para salir.")
        streaming_pull_future.result()
    except KeyboardInterrupt:
        logging.info("Suscripción interrumpida. Apagando...")
        streaming_pull_future.cancel()
        subscriber.close()
    except Exception as e:
        logging.error(f"Excepción del suscriptor: {e}")
        streaming_pull_future.cancel()
        subscriber.close()

