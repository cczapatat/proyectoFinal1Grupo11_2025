import pytest
from unittest.mock import patch, MagicMock
from app.pubsub.consumer import consume_messages, callback, process_message

@pytest.fixture
def mock_pubsub():
    with patch("app.pubsub.consumer.subscriber") as mock_subscriber, \
         patch("app.pubsub.consumer.subscription_path") as mock_subscription_path:
        mock_subscription_path.return_value = "mock_subscription_path"
        mock_subscriber.subscribe.return_value = MagicMock()
        yield mock_subscriber

@pytest.fixture
def mock_db_session():
    with patch("app.pubsub.consumer.SessionLocal") as mock_session:
        mock_instance = MagicMock()
        mock_session.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_repo():
    with patch("app.pubsub.consumer.VideoRecommendationRepository") as mock_repo:
        yield mock_repo

@pytest.mark.asyncio
async def test_process_message_valid(mock_repo):
    message_data = {
        "video_id": "test_video_id",
        "document_id": "test_document_id",
        "tags": "tag1,tag2"
    }

    await process_message(message_data)

    mock_repo.assert_called_once()
    mock_repo.return_value.create_recommendation.assert_called_once_with(
        "test_video_id", "test_document_id", "tag1,tag2"
    )

@pytest.mark.asyncio
async def test_process_message_invalid():
    message_data = {"invalid_key": "value"}

    with patch("app.pubsub.consumer.logging.error") as mock_logging:
        await process_message(message_data)
        mock_logging.assert_called_with(f"Formato de mensaje inválido: {message_data}")

def test_callback_valid():
    message = MagicMock()
    message.data = b'{"video_id": "test_video_id", "document_id": "test_document_id", "tags": "tag1,tag2"}'

    with patch("app.pubsub.consumer.process_message") as mock_process_message:
        callback(message)
        mock_process_message.assert_called_once()
        message.ack.assert_called_once()

def test_callback_invalid():
    message = MagicMock()
    message.data = b'invalid_json'

    with patch("app.pubsub.consumer.logging.error") as mock_logging:
        callback(message)
        mock_logging.assert_called()
        message.ack.assert_called_once()

def test_consume_messages_no_pubsub():
    with patch("app.pubsub.consumer.pubsub_available", False), \
         patch("app.pubsub.consumer.logging.info") as mock_logging:
        consume_messages()
        mock_logging.assert_called_with("PubSub no disponible. Ejecutando en modo de desarrollo.")

def test_consume_messages_with_pubsub(mock_pubsub):
    with patch("app.pubsub.consumer.pubsub_available", True), \
         patch("app.pubsub.consumer.subscriber.subscribe") as mock_subscribe, \
         patch("app.pubsub.consumer.logging.info") as mock_logging:
        mock_subscribe.return_value = MagicMock()
        consume_messages()
        mock_logging.assert_any_call("Escuchando mensajes. Presione Ctrl+C para salir.")
        mock_subscribe.assert_called_once()

def test_callback_error_handling():
    message = MagicMock()
    message.data = b'invalid_json'

    with patch("app.pubsub.consumer.logging.error") as mock_logging:
        callback(message)
        mock_logging.assert_called_with("Error al procesar el mensaje: Expecting value: line 1 column 1 (char 0)")
        message.ack.assert_called_once()

def test_callback_ack_on_exception():
    message = MagicMock()
    message.data = b'{"video_id": "test_video_id"}'

    with patch("app.pubsub.consumer.process_message", side_effect=Exception("Test Exception")) as mock_process_message, \
         patch("app.pubsub.consumer.logging.error") as mock_logging:
        callback(message)
        mock_process_message.assert_called_once()
        mock_logging.assert_called_with("Error al procesar el mensaje: Test Exception")
        message.ack.assert_called_once()

import app.pubsub.consumer  # Ensure the app module is imported for reload

def test_pubsub_initialization_failure():
    with patch("app.pubsub.consumer.pubsub_v1.SubscriberClient", side_effect=Exception("Initialization Error")) as mock_subscriber, \
         patch("app.pubsub.consumer.logging.warning") as mock_logging:
        from importlib import reload
        reload(app.pubsub.consumer)
        mock_logging.assert_called_with("Inicialización de PubSub fallida: Initialization Error. Ejecutando en modo de desarrollo sin PubSub.")