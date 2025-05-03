import json
import pytest

from faker import Faker
from unittest.mock import MagicMock, patch
from manufacturers_worker.models.Operations import BULK_STATUS
from manufacturers_worker.models.bulk_task_model import BulkTask
from manufacturers_worker.models.manufacturer_model import Manufacturer, MANUFACTURER_COUNTRY
from manufacturers_worker.process import process_manufacturers, log_error
from manufacturers_worker.models.declarative_base import session
import manufacturers_worker.init_bd


class TestProcess:
    def setup_method(self):
        self.data_factory = Faker()
        self.process_id = str(self.data_factory.uuid4())
        self.file_id = str(self.data_factory.uuid4())
        self.user_id = str(self.data_factory.uuid4())
        session.rollback()
        session.query(Manufacturer).delete()
        session.query(BulkTask).delete()
        session.commit()

        
    
    @pytest.fixture
    def mock_message(self):
        """Fixture to mock a Pub/Sub message."""
        message = MagicMock()
        message.data = json.dumps({
            "operation": "CREATE",
            "entity_type": "MANUFACTURE",
            "transaction_id": self.process_id,
            "entities": [
                {
                    "name": self.data_factory.name(),
                    "address": self.data_factory.address(),
                    "phone": '+5730054367' + str(self.data_factory.random_int(min=1000, max=9999)),
                    "email": self.data_factory.email(),
                    "country": self.data_factory.random_element(
                        [country.value for country in MANUFACTURER_COUNTRY]),
                    "tax_conditions": self.data_factory.text(),
                    "legal_conditions": self.data_factory.text(),
                    "rating_quality": self.data_factory.random_int(min=0, max=5),
                },
                {
                    "name": self.data_factory.name(),
                    "address": self.data_factory.address(),
                    "phone": '+5730054367' + str(self.data_factory.random_int(min=1000, max=9999)),
                    "email": self.data_factory.email(),
                    "country": self.data_factory.random_element(
                        [country.value for country in MANUFACTURER_COUNTRY]),
                    "tax_conditions": self.data_factory.text(),
                    "legal_conditions": self.data_factory.text(),
                    "rating_quality": self.data_factory.random_int(min=0, max=5),
                }
            ]
        }).encode("utf-8")
        return message
    
    @patch("manufacturers_worker.process.bulk_task_repository.update_bulk_task_status")
    def test_process_create_manufacturer_success(self, mock_update_bulk_task_status, mock_message):
        mock_update_bulk_task_status.return_value = True
        
        process_manufacturers(mock_message)

        mock_update_bulk_task_status.assert_called_once_with(
            self.process_id,
            BULK_STATUS.BULK_COMPLETED
        )
        mock_message.ack.assert_called_once()
    
    @patch("manufacturers_worker.process.manufacturer_repository.create_massive_manufacturers")
    @patch("manufacturers_worker.process.bulk_task_repository.update_bulk_task_status")
    def test_process_create_manufacturer_empty(self, mock_update_bulk_task_status, mock_create_massive_manufacturers, mock_message):
        mock_update_bulk_task_status.return_value = True

        mock_create_massive_manufacturers.return_value = [
        ]
        
        process_manufacturers(mock_message)
        
        mock_create_massive_manufacturers.assert_called_once()
        mock_update_bulk_task_status.assert_called_once_with(
            self.process_id,
            BULK_STATUS.BUlK_FAILED
        )
        mock_message.ack.assert_called_once()
        assert mock_create_massive_manufacturers.call_count == 1
    
    @patch("manufacturers_worker.process.manufacturer_repository.create_massive_manufacturers")
    @patch("manufacturers_worker.process.bulk_task_repository.update_bulk_task_status")
    def test_process_create_manufacturer_exception(self, mock_update_bulk_task_status, mock_create_massive_manufacturers, mock_message):
        mock_update_bulk_task_status.return_value = True

        mock_create_massive_manufacturers.side_effect = Exception("Test exception")
        
        process_manufacturers(mock_message)
        
        mock_create_massive_manufacturers.assert_called_once()
        mock_update_bulk_task_status.assert_not_called()
        mock_message.ack.assert_called_once()
        assert mock_create_massive_manufacturers.call_count == 1
    
    @patch("manufacturers_worker.process.manufacturer_repository.create_massive_manufacturers")
    @patch("manufacturers_worker.process.bulk_task_repository.update_bulk_task_status")
    def test_process_create_manufacturer_invalid_entity_type(self, mock_update_bulk_task_status, mock_create_massive_manufacturers, mock_message):
        mock_message.data = json.dumps({
            "entity_type": "INVALID_ENTITY_TYPE",
            "process_id": self.process_id,
            "entities": [
            ]
        }).encode("utf-8")
        
        process_manufacturers(mock_message)
        
        mock_create_massive_manufacturers.assert_not_called()
        mock_update_bulk_task_status.assert_not_called()
        mock_message.ack.assert_called_once()
    
    @patch("manufacturers_worker.process.manufacturer_repository.create_massive_manufacturers")
    @patch("manufacturers_worker.process.bulk_task_repository.update_bulk_task_status")
    def test_process_create_manufacturer_invalid_operation(self, mock_update_bulk_task_status, mock_create_massive_manufacturers, mock_message):
        mock_message.data = json.dumps({
            "entity_type": "PRODUCT",
            "process_id": self.process_id,
            "operation": "INVALID_OPERATION",
            "entities": [
            ]
        }).encode("utf-8")
        
        process_manufacturers(mock_message)
        
        mock_create_massive_manufacturers.assert_not_called()
        mock_update_bulk_task_status.assert_not_called()
        mock_message.ack.assert_called_once()
    
    @patch("manufacturers_worker.process.manufacturer_repository.create_massive_manufacturers")
    @patch("manufacturers_worker.process.bulk_task_repository.update_bulk_task_status")
    def test_process_create_manufacturer_invalid_json(self, mock_update_bulk_task_status, mock_create_massive_manufacturers, mock_message):
        mock_message.data = b"invalid json"
        
        process_manufacturers(mock_message)
        
        mock_create_massive_manufacturers.assert_not_called()
        mock_update_bulk_task_status.assert_not_called()
        mock_message.ack.assert_called_once()
    
    @patch("builtins.print")
    def test_log_error(self, mock_print):
        log_error("Test Context", self.process_id, Exception("Test exception"))

        mock_print.assert_called_once_with(f"[Test Context] process_id: {self.process_id}, error: Test exception")