import json
import io
from faker import Faker
from unittest.mock import MagicMock, patch
from document_manager import application as app


class TestDocument:
    def setup_method(self):
        self.data_factory = Faker()
        self.test_client = app.test_client()

    def _create_fake_file(self, content="name,age\nJohn,30\nDoe,25", filename="test.csv", content_type="text/csv"):
        fake_file = io.BytesIO(content.encode("utf-8"))
        fake_file.filename = filename
        fake_file.content_type = content_type
        return fake_file

    def _post_document(self, file, authorization=None, token="internal_token"):
        data = {} if file is None else {"file": (file, file.filename)}
        headers = {}
            
        if token != None:
            headers["x-token"] = token

        if authorization != None:
            headers["Authorization"] = authorization

        return self.test_client.post(
            "/document-manager/document/create",
            data=data,
            headers=headers,
            content_type="multipart/form-data",
        )

    def _get_document(self, document_id, user_id, token="internal_token"):
        headers = {
            "x-token": token,
            "user-id": str(user_id),
        }
        return self.test_client.get(
            f"/document-manager/document/{document_id}", headers=headers
        )

    def _get_document_file(self, document_id, user_id, token="internal_token"):
        headers = {
            "x-token": token,
            "user-id": str(user_id),
        }
        return self.test_client.get(
            f"/document-manager/document/{document_id}/file", headers=headers
        )

    def test_health(self):
        response = self.test_client.get("/document-manager/health")
        assert response.status_code == 200
        assert b'{"status":"up"}' in response.data
      
    def test_create_document_without_authorization(self):
        fake_file = self._create_fake_file()
        response = self._post_document(fake_file)
        assert response.status_code == 401
        assert b"Unauthorized" in response.data
      
    @patch("document_manager.api.documents.__validate_auth_token")
    def test_create_document_without_internal_token(self, mock_validate_auth_token):
        fake_user_id = self.data_factory.uuid4()
        fake_authorization = self.data_factory.uuid4()
        mock_validate_auth_token.return_value = {
            "user_type": "ADMIN",
            "user_session_id": fake_user_id,
        }

        fake_file = self._create_fake_file()
        response = self._post_document(fake_file, fake_authorization, token=None)
        assert response.status_code == 401
        assert b"Unauthorized" in response.data
      
    @patch("document_manager.api.documents.__validate_auth_token")
    def test_create_document_bad_internal_token(self, mock_validate_auth_token):
        fake_user_id = self.data_factory.uuid4()
        fake_authorization = self.data_factory.uuid4()
        mock_validate_auth_token.return_value = {
            "user_type": "ADMIN",
            "user_session_id": fake_user_id,
        }

        fake_file = self._create_fake_file()
        response = self._post_document(fake_file, fake_authorization, token="bad_token")
        assert response.status_code == 401
        assert b"Unauthorized" in response.data
    
    @patch("document_manager.api.documents.requests.get")
    def test_create_document_auth_response_unauthorized(self, mock_requests_get):
        fake_authorization = self.data_factory.uuid4()

        mock_response = MagicMock()
        mock_response.status_code = 401 
        mock_requests_get.return_value = mock_response

        fake_file = self._create_fake_file()
        response = self._post_document(fake_file, fake_authorization)

        assert response.status_code == 401
        assert b"authorization required" in response.data
      
    @patch("document_manager.api.documents.requests.get")
    def test_create_document_auth_response_internal_server_error(self, mock_requests_get):
        fake_authorization = self.data_factory.uuid4()
        
        mock_response = MagicMock()
        mock_response.status_code = 500  
        mock_requests_get.return_value = mock_response

        fake_file = self._create_fake_file()
        response = self._post_document(fake_file, fake_authorization)

        assert response.status_code == 500
        assert b"internal server error on user_session_manager" in response.data
    
    @patch("document_manager.api.documents.__validate_auth_token")
    def test_create_document_success_by_seller(self, mock_validate_auth_token):
        fake_user_id = self.data_factory.uuid4()
        fake_authorization = self.data_factory.uuid4()
        mock_validate_auth_token.return_value = {
            "user_type": "SELLER",
            "user_id": fake_user_id,
        }

        fake_file = self._create_fake_file()

        response = self._post_document(fake_file, fake_authorization)

        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert "id" in response_data
        assert response_data["user_id"] == fake_user_id
    
    @patch("document_manager.api.documents.__validate_auth_token")
    def test_create_document_error_user_id_required(self, mock_validate_auth_token):
        fake_user_id = self.data_factory.uuid4()
        fake_authorization = self.data_factory.uuid4()
        mock_validate_auth_token.return_value = {
            "user_type": "SELLER",
            "user_id": None,
        }

        fake_file = self._create_fake_file()

        response = self._post_document(fake_file, fake_authorization)

        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert "message" in response_data
        assert response_data["message"] == "user-id is required"

    @patch("document_manager.api.documents.__validate_auth_token")
    def test_create_document_success(self, mock_validate_auth_token):
        fake_user_id = self.data_factory.uuid4()
        fake_authorization = self.data_factory.uuid4()
        mock_validate_auth_token.return_value = {
            "user_type": "ADMIN",
            "user_session_id": fake_user_id,
        }

        fake_file = self._create_fake_file()

        response = self._post_document(fake_file, fake_authorization)

        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert "id" in response_data
        assert response_data["user_id"] == fake_user_id

    @patch("document_manager.api.documents.__validate_auth_token")
    def test_create_document_missing_file(self, mock_validate_auth_token):
        fake_user_id = self.data_factory.uuid4()
        fake_authorization = self.data_factory.uuid4()
        mock_validate_auth_token.return_value = {
            "user_type": "ADMIN",
            "user_session_id": "12345",
        }
        response = self._post_document(None, fake_user_id)

        assert response.status_code == 400
        assert b"No file part" in response.data

    @patch("document_manager.api.documents.__validate_auth_token")
    def test_create_document_invalid_file_extension(self, mock_validate_auth_token):
        fake_user_id = self.data_factory.uuid4()
        fake_authorization = self.data_factory.uuid4()
        mock_validate_auth_token.return_value = {
            "user_type": "ADMIN",
            "user_session_id": fake_user_id,
        }

        fake_file = self._create_fake_file(filename="test.txt")

        response = self._post_document(fake_file, fake_authorization)

        assert response.status_code == 400
        assert b"Invalid file extension" in response.data

    @patch("document_manager.api.documents.__validate_auth_token")
    def test_create_document_filename_empty(self, mock_validate_auth_token):
        fake_user_id = self.data_factory.uuid4()
        mock_validate_auth_token.return_value = {
            "user_type": "ADMIN",
            "user_session_id": fake_user_id,
        }

        fake_file = self._create_fake_file(filename="")

        response = self._post_document(fake_file, fake_user_id)

        assert response.status_code == 400
        assert b"No selected file" in response.data

    @patch("document_manager.api.documents.__validate_auth_token")
    def test_create_document_upload_error(self, mock_validate_auth_token):
        fake_user_id = self.data_factory.uuid4()
        fake_authorization = self.data_factory.uuid4()
        mock_validate_auth_token.return_value = {
            "user_type": "ADMIN",
            "user_session_id": fake_user_id,
        }

        fake_file = self._create_fake_file()

        with patch(
            "document_manager.api.documents.cloud_storage_repository.upload_file",
            return_value=None,
        ):
            response = self._post_document(fake_file, fake_authorization)

            assert response.status_code == 500
            assert b"Error uploading file" in response.data

    @patch("document_manager.api.documents.__validate_auth_token")
    def test_create_document_invalid_user_type(self, mock_validate_auth_token):
        fake_user_id = self.data_factory.uuid4()
        fake_authorization = self.data_factory.uuid4()
        mock_validate_auth_token.return_value = {
            "user_type": "UNKNOWN",
            "user_session_id": fake_user_id,
        }

        fake_file = self._create_fake_file()

        response = self._post_document(fake_file, fake_authorization)

        assert response.status_code == 403
        assert b"Invalid user type" in response.data

    @patch("document_manager.api.documents.__validate_auth_token")
    def test_get_document_by_id_success(self, mock_validate_auth_token):
        fake_user_id = self.data_factory.uuid4()
        fake_authorization = self.data_factory.uuid4()
        mock_validate_auth_token.return_value = {
            "user_type": "ADMIN",
            "user_session_id": fake_user_id,
        }
        fake_file = self._create_fake_file()

        create_response = self._post_document(fake_file, fake_authorization)
        assert create_response.status_code == 201

        response_data_create = json.loads(create_response.data)
        response = self._get_document(response_data_create["id"], fake_user_id)

        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data["id"] == str(response_data_create["id"])
        assert response_data["user_id"] == str(fake_user_id)

    @patch("document_manager.api.documents.__validate_auth_token")  
    def test_get_document_by_id_not_found(self, mock_validate_auth_token):
        fake_user_id = self.data_factory.uuid4()
        fake_authorization = self.data_factory.uuid4()
        mock_validate_auth_token.return_value = {
            "user_type": "ADMIN",
            "user_session_id": fake_user_id,
        }
        fake_document_id = self.data_factory.uuid4()

        response = self._get_document(fake_document_id, fake_user_id)

        assert response.status_code == 404
        assert b"Document not found" in response.data

    def test_get_document_by_id_invalid_id(self):
        fake_user_id = self.data_factory.uuid4()
        fake_document_id = "invalid_uuid"

        response = self._get_document(fake_document_id, fake_user_id)

        assert response.status_code == 400
        assert b"Invalid document id" in response.data

    @patch("document_manager.api.documents.__validate_auth_token")
    def test_get_document_file_by_id_success(self, mock_validate_auth_token):
        fake_user_id = self.data_factory.uuid4()
        mock_validate_auth_token.return_value = {
            "user_type": "ADMIN",
            "user_session_id": fake_user_id,
        }
        fake_file = self._create_fake_file()
        

        create_response = self._post_document(fake_file, fake_user_id)
        assert create_response.status_code == 201

        response_data_create = json.loads(create_response.data)
        response = self._get_document_file(response_data_create["id"], fake_user_id)

        assert response.status_code == 200
        assert b"name,age\nJohn,30\nDoe,25" in response.data

    def test_get_document_file_by_id_not_found(self):
        fake_user_id = self.data_factory.uuid4()
        fake_document_id = self.data_factory.uuid4()

        response = self._get_document_file(fake_document_id, fake_user_id)

        assert response.status_code == 404
        assert b"Document not found" in response.data
        
    @patch("document_manager.api.documents.__validate_auth_token")
    def test_get_document_file_by_id_download_fail(self, mock_validate_auth_token):
        fake_user_id = self.data_factory.uuid4()
        mock_validate_auth_token.return_value = {
            "user_type": "ADMIN",
            "user_session_id": fake_user_id,
        }
        fake_file = self._create_fake_file()
        
        create_response = self._post_document(fake_file, fake_user_id)
        assert create_response.status_code == 201

        response_data_create = json.loads(create_response.data)

        with patch(
            "document_manager.api.documents.cloud_storage_repository.download_file",
            return_value=(None, None),
        ):
            response = self._get_document_file(response_data_create["id"], fake_user_id)

            assert response.status_code == 409
            assert b"Download fail" in response.data