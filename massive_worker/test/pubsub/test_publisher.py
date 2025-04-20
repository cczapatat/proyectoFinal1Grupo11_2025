import pytest
from unittest.mock import patch, MagicMock
from massive_worker.pubsub.publisher import Publisher

class TestPublisher:
    @patch("massive_worker.pubsub.publisher.publisher_retry_attempt.publish")
    def test_publish_retry_attempt(self, mock_publish):
        # Mock the publish method
        mock_future = MagicMock()
        mock_future.result.return_value = "mock_message_id"
        mock_publish.return_value = mock_future

        publisher = Publisher()
        mock_message = MagicMock()
        mock_message.data = b"test_message"

        # Call the method
        publisher.publish_retry_attempt(mock_message)

        # Assertions
        mock_publish.assert_called_once_with(
            "projects/proyectofinalmiso2025/topics/commands_to_massive",
            b"test_message"
        )
        mock_future.result.assert_called_once()

    @patch("massive_worker.pubsub.publisher.publisher_massive_entity.publish")
    @patch("massive_worker.pubsub.publisher.entity_batch_repository.create_entity_batch")
    @patch("massive_worker.pubsub.publisher.entity_batch_repository.get_last_entity_batch")
    def test_publish_massive_entity_success(self, mock_get_last_batch, mock_create_batch, mock_publish):
        # Mock dependencies
        mock_get_last_batch.return_value = None
        mock_future = MagicMock()
        mock_future.result.return_value = "mock_message_id"
        mock_publish.return_value = mock_future

        publisher = Publisher()
        json_data = [{"key": "value"} for _ in range(150)]  # Simulate 150 rows of data

        # Call the method
        publisher.publish_massive_entity(
            entity_type="PRODUCT",
            operation="CREATE",
            process_id="test_process_id",
            file_id="test_file_id",
            user_id="test_user_id",
            json_data=json_data
        )

        # Assertions
        assert mock_publish.call_count == 2  # Two batches of 100 rows each
        mock_create_batch.assert_called()
        mock_get_last_batch.assert_called_once_with("test_process_id")

    def test_get_publisher_retry_attempt(self):
        publisher = Publisher()
        result = publisher.get_publisher_retry_attempt()

        assert result is not None