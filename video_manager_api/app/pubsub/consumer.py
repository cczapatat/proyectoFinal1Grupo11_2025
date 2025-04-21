import os
import json
import logging
from google.cloud import pubsub_v1
from app.mappers.pubsub_mapper import map_pubsub_message_to_video_simulations
from app.uow.unit_of_work import UnitOfWork
from app.repositories.video_recomendation_repository import VideoRecomendationRepository

GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "proyectofinalmiso2025")
VIDEO_RECOMMENDATION_SUB = os.environ.get("GCP_VIDEO_RECOMMENDATION_SUB", "video_to_recommendation-sub")

# Flag to track if PubSub is available
pubsub_available = False
subscriber = None
subscription_path = None

try:
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(GCP_PROJECT_ID, VIDEO_RECOMMENDATION_SUB)
    pubsub_available = True
except Exception as e:
    logging.warning(f"PubSub initialization failed: {e}. Running in development mode without PubSub.")


def callback(message):
    try:
        print(" === Inicia procesamiento de recomendación de video ===")
        print(f" > Mensaje recibido: {message.data}")
        payload = json.loads(message.data.decode("utf-8"))
        video_simulation_dto = map_pubsub_message_to_video_simulations([payload])[0]  # Map the message to DTO
        with UnitOfWork() as uow:
            repo = VideoRecomendationRepository(uow.session)
            repo.create_recommendation(video_simulation_dto)  # Call the repository method
            print(" === Procesamiento de recomendación de video completado ===")
        message.ack()
    except Exception as e:
        print(f"Error al procesar mensaje: {e}")
        message.ack()  # TODO: Consider implementing NACK handling


def consume_messages():
    if not pubsub_available:
        print("PubSub not available. Running in development mode without message consumption.")
        return
    
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Escuchando mensajes en {subscription_path}...")
    try:
        streaming_pull_future.result()
    except Exception as e:
        print(f"Excepción en el suscriptor: {e}")
        streaming_pull_future.cancel()
