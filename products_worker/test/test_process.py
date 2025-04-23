import json
import pytest

from faker import Faker
from unittest.mock import MagicMock, patch
from products_worker.models.Operations import BULK_STATUS
from products_worker.models.bulk_task_model import BulkTask
from products_worker.models.product_model import CATEGORY_PRODUCT, CURRENCY_PRODUCT, Product
from products_worker.process import process_products, log_error
from products_worker.models.declarative_base import session


class TestProcess:
    def setup_method(self):
        self.data_factory = Faker()
        self.process_id = str(self.data_factory.uuid4())
        self.file_id = str(self.data_factory.uuid4())
        self.user_id = str(self.data_factory.uuid4())
        session.rollback()
        session.query(Product).delete()
        session.query(BulkTask).delete()
        session.commit()

        
    
    @pytest.fixture
    def mock_message(self):
        """Fixture to mock a Pub/Sub message."""
        message = MagicMock()
        message.data = json.dumps({
            "operation": "CREATE",
            "entity_type": "PRODUCT",
            "transaction_id": self.process_id,
            "entities": [
                {
                    "manufacturer_id": self.data_factory.uuid4(),
                    "name": self.data_factory.word(),
                    "description": self.data_factory.word(),
                    "category": self.data_factory.random_element(
                        [category.value for category in CATEGORY_PRODUCT]
                    ),
                    "unit_price": 100,
                    "currency_price": self.data_factory.random_element(
                        [currency.value for currency in CURRENCY_PRODUCT]
                    ),
                    "is_promotion": self.data_factory.boolean(),
                    "discount_price": self.data_factory.random_number(digits=2),
                    "expired_at": None,
                    "url_photo": self.data_factory.image_url(),
                    "store_conditions": self.data_factory.word()
                },
                {
                    "manufacturer_id": self.data_factory.uuid4(),
                    "name": self.data_factory.word(),
                    "description": self.data_factory.word(),
                    "category": self.data_factory.random_element(
                        [category.value for category in CATEGORY_PRODUCT]
                    ),
                    "unit_price": 100,
                    "currency_price": self.data_factory.random_element(
                        [currency.value for currency in CURRENCY_PRODUCT]
                    ),
                    "is_promotion": self.data_factory.boolean(),
                    "discount_price": self.data_factory.random_number(digits=2),
                    "expired_at": None,
                    "url_photo": self.data_factory.image_url(),
                    "store_conditions": self.data_factory.word()
                }
            ]
        }).encode("utf-8")
        return message
    
    @patch("products_worker.process.bulk_task_repository.update_bulk_task_status")
    def test_process_create_product_success(self, mock_update_bulk_task_status, mock_message):
        mock_update_bulk_task_status.return_value = True
        
        process_products(mock_message)

        mock_update_bulk_task_status.assert_called_once_with(
            self.process_id,
            BULK_STATUS.BULK_COMPLETED
        )
        mock_message.ack.assert_called_once()
    
    @patch("products_worker.process.product_repository.create_massive_products")
    @patch("products_worker.process.bulk_task_repository.update_bulk_task_status")
    def test_process_create_product_empty(self, mock_update_bulk_task_status, mock_create_massive_products, mock_message):
        mock_update_bulk_task_status.return_value = True

        mock_create_massive_products.return_value = [
        ]
        
        process_products(mock_message)
        
        mock_create_massive_products.assert_called_once()
        mock_update_bulk_task_status.assert_called_once_with(
            self.process_id,
            BULK_STATUS.BUlK_FAILED
        )
        mock_message.ack.assert_called_once()
        assert mock_create_massive_products.call_count == 1
    
    @patch("products_worker.process.product_repository.create_massive_products")
    @patch("products_worker.process.bulk_task_repository.update_bulk_task_status")
    def test_process_create_product_exception(self, mock_update_bulk_task_status, mock_create_massive_products, mock_message):
        mock_update_bulk_task_status.return_value = True

        mock_create_massive_products.side_effect = Exception("Test exception")
        
        process_products(mock_message)
        
        mock_create_massive_products.assert_called_once()
        mock_update_bulk_task_status.assert_not_called()
        mock_message.ack.assert_called_once()
        assert mock_create_massive_products.call_count == 1
    
    @patch("products_worker.process.product_repository.create_massive_products")
    @patch("products_worker.process.bulk_task_repository.update_bulk_task_status")
    def test_process_create_product_invalid_entity_type(self, mock_update_bulk_task_status, mock_create_massive_products, mock_message):
        mock_message.data = json.dumps({
            "entity_type": "INVALID_ENTITY_TYPE",
            "process_id": self.process_id,
            "entities": [
            ]
        }).encode("utf-8")
        
        process_products(mock_message)
        
        mock_create_massive_products.assert_not_called()
        mock_update_bulk_task_status.assert_not_called()
        mock_message.ack.assert_called_once()
    
    @patch("products_worker.process.product_repository.create_massive_products")
    @patch("products_worker.process.bulk_task_repository.update_bulk_task_status")
    def test_process_create_product_invalid_operation(self, mock_update_bulk_task_status, mock_create_massive_products, mock_message):
        mock_message.data = json.dumps({
            "entity_type": "PRODUCT",
            "process_id": self.process_id,
            "operation": "INVALID_OPERATION",
            "entities": [
            ]
        }).encode("utf-8")
        
        process_products(mock_message)
        
        mock_create_massive_products.assert_not_called()
        mock_update_bulk_task_status.assert_not_called()
        mock_message.ack.assert_called_once()
    
    @patch("products_worker.process.product_repository.create_massive_products")
    @patch("products_worker.process.bulk_task_repository.update_bulk_task_status")
    def test_process_create_product_invalid_json(self, mock_update_bulk_task_status, mock_create_massive_products, mock_message):
        mock_message.data = b"invalid json"
        
        process_products(mock_message)
        
        mock_create_massive_products.assert_not_called()
        mock_update_bulk_task_status.assert_not_called()
        mock_message.ack.assert_called_once()
    
    @patch("builtins.print")
    def test_log_error(self, mock_print):
        log_error("Test Context", self.process_id, Exception("Test exception"))

        mock_print.assert_called_once_with(f"[Test Context] process_id: {self.process_id}, error: Test exception")