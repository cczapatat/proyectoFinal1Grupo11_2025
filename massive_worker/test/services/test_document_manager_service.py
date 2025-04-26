from unittest.mock import patch, MagicMock
import massive_worker.init_bd
from massive_worker.services.document_manager_service import DocumentManagerService

class TestDocumentManagerService:
    @patch("massive_worker.services.document_manager_service.requests.get")
    def test_get_json_from_document_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "column1,column2\nvalue1,value2\nvalue3,value4"
        mock_get.return_value = mock_response

        service = DocumentManagerService()
        result = service.get_json_from_document("test_file_id")

        # Assertions
        mock_get.assert_called_once()

        assert result == [
            {"column1": "value1", "column2": "value2"},
            {"column1": "value3", "column2": "value4"}
        ]

    @patch("massive_worker.services.document_manager_service.requests.get")
    def test_get_json_from_document_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        service = DocumentManagerService()
        result = service.get_json_from_document("test_file_id")

        mock_get.assert_called_once()
        assert result is None