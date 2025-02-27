import unittest
import uuid
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import IntegrityError

from manufacturers_worker.src.models.model import Manufacturer, Error
from manufacturers_worker.src.services.manufacturer_service import ManufacturerService

class TestManufacturerService(unittest.TestCase):
    """Test the ManufacturerService class"""
    
    def setUp(self):
        """Set up for the tests"""
        self.service = ManufacturerService()
        self.transaction_id = uuid.uuid4()
        self.batch_number = 1
        
        # Valid manufacturer data
        self.valid_manufacturer = {
            "nombre": "Test Manufacturer",
            "nit": "123456789",
            "direccion": "Test Address",
            "telefono": "1234567890",
            "correo": "test@example.com",
            "codigo_pais": "CO"
        }
        
        # Invalid manufacturer data (missing required field)
        self.invalid_manufacturer = {
            "nombre": "Test Manufacturer",
            "nit": "123456789",
            "direccion": "Test Address",
            "telefono": "1234567890",
            # Missing correo
            "codigo_pais": "CO"
        }
        
        # Invalid manufacturer data (field too long)
        self.invalid_code_manufacturer = {
            "nombre": "Test Manufacturer",
            "nit": "123456789",
            "direccion": "Test Address",
            "telefono": "1234567890",
            "correo": "test@example.com",
            "codigo_pais": "USA"  # Too long
        }

    @patch('manufacturers_worker.src.services.manufacturer_service.db.session')
    def test_process_batch_valid_manufacturer(self, mock_session):
        """Test processing a batch with a valid manufacturer"""
        # Test data
        manufacturers = [self.valid_manufacturer]
        
        # Call the method
        self.service.process_batch(self.transaction_id, self.batch_number, manufacturers)
        
        # Verify
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.rollback.assert_not_called()

    @patch('manufacturers_worker.src.services.manufacturer_service.db.session')
    def test_process_batch_missing_field(self, mock_session):
        """Test processing a batch with an invalid manufacturer (missing field)"""
        # Test data
        manufacturers = [self.invalid_manufacturer]
        
        # Call the method
        self.service.process_batch(self.transaction_id, self.batch_number, manufacturers)
        
        # Verify error handling
        mock_session.add.assert_called_once()  # For the error record
        mock_session.commit.assert_called_once()
        
        # Get the error instance that was added
        error_record = mock_session.add.call_args[0][0]
        self.assertIsInstance(error_record, Error)
        self.assertEqual(error_record.transaction_id, self.transaction_id)
        self.assertEqual(error_record.batch_number, self.batch_number)
        self.assertEqual(error_record.line_number, 1)
        self.assertIn("correo is required", error_record.description)

    @patch('manufacturers_worker.src.services.manufacturer_service.db.session')
    def test_process_batch_field_too_long(self, mock_session):
        """Test processing a batch with an invalid manufacturer (field too long)"""
        # Test data
        manufacturers = [self.invalid_code_manufacturer]
        
        # Call the method
        self.service.process_batch(self.transaction_id, self.batch_number, manufacturers)
        
        # Verify error handling
        mock_session.add.assert_called_once()  # For the error record
        mock_session.commit.assert_called_once()
        
        # Get the error instance that was added
        error_record = mock_session.add.call_args[0][0]
        self.assertIsInstance(error_record, Error)
        self.assertEqual(error_record.transaction_id, self.transaction_id)
        self.assertEqual(error_record.batch_number, self.batch_number)
        self.assertEqual(error_record.line_number, 1)
        self.assertIn("codigo_pais must be 2 characters", error_record.description)

    @patch('manufacturers_worker.src.services.manufacturer_service.db.session')
    def test_process_batch_duplicate_record(self, mock_session):
        """Test processing a batch with a duplicate manufacturer (same nombre and nit)"""
        # Test data
        manufacturers = [self.valid_manufacturer]
        
        # Mock IntegrityError when trying to commit
        mock_session.commit.side_effect = [IntegrityError(None, None, None), None]
        
        # Call the method
        self.service.process_batch(self.transaction_id, self.batch_number, manufacturers)
        
        # Verify error handling
        self.assertEqual(mock_session.add.call_count, 2)  # One for manufacturer, one for error
        self.assertEqual(mock_session.commit.call_count, 2)  # One failed, one for error record
        self.assertEqual(mock_session.rollback.call_count, 1)
        
        # Get the error instance that was added (second call to add)
        error_record = mock_session.add.call_args[0][0]
        self.assertIsInstance(error_record, Error)
        self.assertEqual(error_record.transaction_id, self.transaction_id)
        self.assertEqual(error_record.batch_number, self.batch_number)
        self.assertEqual(error_record.line_number, 1)
        self.assertIn("nombre and nit are already saved", error_record.description)

    @patch('manufacturers_worker.src.services.manufacturer_service.db.session')
    def test_process_batch_multiple_manufacturers(self, mock_session):
        """Test processing a batch with multiple manufacturers"""
        # Test data - one valid, one invalid
        manufacturers = [self.valid_manufacturer, self.invalid_manufacturer]
        
        # Mock so that first commit succeeds but second one fails with validation error
        def side_effect(*args, **kwargs):
            # This will be called for each add depending on the manufacturer
            added_object = mock_session.add.call_args[0][0]
            if isinstance(added_object, Error):
                return None  # For Error objects, succeed
            
            # For the second manufacturer (which is invalid), simulate validation issue
            if mock_session.add.call_count > 1:
                from marshmallow import ValidationError
                raise ValidationError({"correo": "correo is required"})
        
        # Call the method
        with patch.object(self.service.manufacturer_schema, 'load', side_effect=side_effect):
            self.service.process_batch(self.transaction_id, self.batch_number, manufacturers)
        
        # Verify results
        self.assertEqual(mock_session.add.call_count, 2)  # One for valid manufacturer, one for error
        
if __name__ == '__main__':
    unittest.main()