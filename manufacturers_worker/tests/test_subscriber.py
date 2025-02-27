import unittest
import json
from unittest.mock import patch, MagicMock

from manufacturers_worker.src.pubsub.subscriber import PubSubSubscriber

class TestPubSubSubscriber(unittest.TestCase):
    """Test the PubSubSubscriber class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_manufacturer_service = MagicMock()
        
        # Mock environment variables
        self.env_patcher = patch.dict(
            'os.environ', 
            {'PROJECT_ID': 'test-project', 'SUBSCRIPTION_ID': 'test-subscription'}
        )
        self.env_patcher.start()
        
        # Create subscriber with mocked service
        with patch('google.cloud.pubsub_v1.SubscriberClient'):
            self.subscriber = PubSubSubscriber(self.mock_manufacturer_service)
            self.subscriber.subscriber = MagicMock()
            self.subscriber.subscription_path = 'projects/test-project/subscriptions/test-subscription'
    
    def tearDown(self):
        """Clean up after tests"""
        self.env_patcher.stop()
    
    def test_init(self):
        """Test subscriber initialization"""
        self.assertEqual(self.subscriber.project_id, 'test-project')
        self.assertEqual(self.subscriber.subscription_id, 'test-subscription')
        self.assertEqual(self.subscriber.manufacturer_service, self.mock_manufacturer_service)
        
    def test_process_message_valid(self):
        """Test processing a valid message"""
        # Test data
        transaction_id = 'test-transaction-id'
        batch_number = 1
        manufacturers = [
            {
                "nombre": "Test Manufacturer",
                "nit": "123456789",
                "direccion": "Test Address",
                "telefono": "1234567890",
                "correo": "test@example.com",
                "codigo_pais": "CO"
            }
        ]
        
        message_data = {
            'transaction_id': transaction_id,
            'batch_number': batch_number,
            'manufacturers': manufacturers
        }
        
        # Create mock message
        mock_message = MagicMock()
        mock_message.data = json.dumps(message_data).encode('utf-8')
        mock_message.message_id = 'test-message-id'
        
        # Call the method
        self.subscriber._process_message(mock_message)
        
        # Verify
        self.mock_manufacturer_service.process_batch.assert_called_once_with(
            transaction_id=transaction_id,
            batch_number=batch_number,
            manufacturers=manufacturers
        )
        mock_message.ack.assert_called_once()

    def test_process_message_with_error(self):
        """Test processing a message that causes an error"""
        # Test data with invalid structure
        message_data = {
            'transaction_id': 'test-transaction-id',
            'batch_number': 'invalid',  # Should be an integer
            'manufacturers': []
        }
        
        # Create mock message
        mock_message = MagicMock()
        mock_message.data = json.dumps(message_data).encode('utf-8')
        mock_message.message_id = 'test-message-id'
        
        # Mock service to raise exception
        self.mock_manufacturer_service.process_batch.side_effect = Exception('Test error')
        
        # Call the method
        self.subscriber._process_message(mock_message)
        
        # Verify - message should not be acknowledged
        mock_message.ack.assert_not_called()

if __name__ == '__main__':
    unittest.main()