import json
import os
from massive_worker.models.attempt import Attempt
from massive_worker.models.attempt_error import AttemptError
from massive_worker.models.entity_batch import EntityBatch
from massive_worker.process import log_error, process_attempts
from massive_worker.models.declarative_base import session
import pytest
from faker import Faker
from unittest.mock import MagicMock, patch

class TestProcess:
    def setup_method(self):
        self.data_factory = Faker()
        self.process_id = str(self.data_factory.uuid4())
        self.file_id = str(self.data_factory.uuid4())
        self.user_id = str(self.data_factory.uuid4())
        session.rollback()
        session.query(AttemptError).delete()
        session.query(EntityBatch).delete()
        session.query(Attempt).delete()
        session.commit()


    @pytest.fixture
    def mock_message(self):
        """Fixture to mock a Pub/Sub message."""
        message = MagicMock()
        message.data = json.dumps({
            "operation": "CREATE",
            "entity": "PRODUCT",
            "process_id": self.process_id,
            "file_id": self.file_id,
            "user_id": self.user_id
        }).encode("utf-8")
        return message

    @patch("massive_worker.process.document_manager_service.get_json_from_document")
    @patch("massive_worker.pubsub.publisher.Publisher.publish_massive_entity")
    def test_process_attempts_success(self,mock_publish, mock_get_json, mock_message):
        mock_get_json.return_value = [{
            "key": "value"
        }]
        process_attempts(mock_message)

        mock_get_json.assert_called_once_with(self.file_id)
        mock_publish.assert_called_once()
        mock_message.ack.assert_called_once()

    @patch("massive_worker.process.document_manager_service.get_json_from_document")
    @patch("massive_worker.process.attempt_repository.create_attempt")
    def test_process_attempts_none(self, mock_create_attempt, mock_get_json, mock_message):
        mock_get_json.return_value = [{"key": "value"}]
        mock_create_attempt.return_value = None

        process_attempts(mock_message)

        mock_get_json.assert_called_once_with(self.file_id)
        mock_create_attempt.assert_called_once_with(
            "CREATE", "PRODUCT", self.process_id, self.file_id, self.user_id
        )
        mock_message.ack.assert_not_called()

    def test_process_attempts_missing_fields(self, mock_message):
        mock_message.data = json.dumps({
            "operation": "CREATE",
            "entity": "PRODUCT"
        }).encode("utf-8")

        process_attempts(mock_message)

        mock_message.ack.assert_not_called()

    @patch("massive_worker.process.document_manager_service.get_json_from_document")
    @patch("massive_worker.process.threading.Timer")
    @patch("massive_worker.pubsub.publisher.Publisher.get_publisher_retry_attempt")
    def test_process_attempts_json_data_none(self, mock_get_publisher_retry, mock_timer, mock_get_json, mock_message):
        mock_get_json.return_value = None
        mock_get_publisher_retry.return_value = MagicMock()

        process_attempts(mock_message)

        mock_get_json.assert_called_once_with(self.file_id)
        mock_timer.assert_called_once()
        mock_timer.assert_called_with(5, mock_get_publisher_retry.return_value.publish_retry_attempt, args=(mock_message,))
        mock_message.ack.assert_called_once()

    @patch("massive_worker.process.document_manager_service.get_json_from_document")
    @patch("massive_worker.process.attempt_error_repository.get_last_attempt_error")
    @patch("massive_worker.process.threading.Timer")
    def test_process_attempts_retry_logic(self, mock_timer, mock_create_error, mock_get_last_error, mock_get_json, mock_message):
        mock_get_json.return_value = None
        mock_get_last_error.return_value = MagicMock(retry_quantity=1)

        process_attempts(mock_message)

        mock_get_last_error.assert_called_once_with(self.process_id)
        mock_create_error.assert_called_once()
        mock_timer.assert_called_once()
        mock_message.ack.assert_called_once()

    @patch("massive_worker.process.document_manager_service.get_json_from_document")
    def test_process_attempts_exception_handling(self, mock_get_json, mock_message):
        mock_get_json.side_effect = Exception("Test exception")

        process_attempts(mock_message)

        mock_message.nack.assert_called_once()

    @patch("builtins.print")
    def test_log_error(self, mock_print):
        log_error("Test Context", self.process_id, Exception("Test exception"))

        mock_print.assert_called_once_with(f"[Test Context] process_id: {self.process_id}, error: Test exception")

    @patch("massive_worker.process.document_manager_service.get_json_from_document")
    @patch("massive_worker.process.attempt_error_repository.get_last_attempt_error")
    @patch("massive_worker.process.attempt_error_repository.create_attempt_error")
    @patch("massive_worker.process.threading.Timer")
    @patch("massive_worker.pubsub.publisher.Publisher.get_publisher_retry_attempt")
    def test_process_attempts_retry_logic(self, mock_get_publisher_retry, mock_timer, mock_create_error, mock_get_last_error, mock_get_json, mock_message):
        mock_get_json.return_value = None
        mock_get_last_error.return_value = MagicMock(retry_quantity=1)
        mock_get_publisher_retry.return_value = MagicMock()

        process_attempts(mock_message)

        mock_get_json.assert_called_once_with(self.file_id)
        mock_get_last_error.assert_called_once_with(self.process_id)
        mock_create_error.assert_called_once_with(
            "CREATE", "PRODUCT",self.process_id, self.file_id, self.user_id, 2
        )
        mock_timer.assert_called_once()
        mock_timer.assert_called_with(10, mock_get_publisher_retry.return_value.publish_retry_attempt, args=(mock_message,))
        mock_message.ack.assert_called_once()

    @patch("massive_worker.process.document_manager_service.get_json_from_document")
    @patch("massive_worker.process.attempt_error_repository.get_last_attempt_error")
    @patch("massive_worker.process.attempt_error_repository.create_attempt_error")
    @patch("massive_worker.process.threading.Timer")
    def test_process_attempts_exceed_max_retries(self, mock_timer, mock_create_error, mock_get_last_error, mock_get_json, mock_message):
        mock_get_json.return_value = None

        mock_get_last_error.return_value = MagicMock(retry_quantity=3)

        process_attempts(mock_message)

        mock_get_json.assert_called_once_with(self.file_id)
        mock_get_last_error.assert_called_once_with(self.process_id)
        mock_create_error.assert_not_called()
        mock_timer.assert_not_called()
        mock_message.ack.assert_called_once()