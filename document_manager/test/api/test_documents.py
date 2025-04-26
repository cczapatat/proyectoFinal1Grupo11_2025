import json
import io
from faker import Faker
from unittest.mock import MagicMock, patch

data_factory = Faker()


def _create_fake_file(content="name,age\nJohn,30\nDoe,25", filename="test.csv", content_type="text/csv"):
    fake_file = io.BytesIO(content.encode("utf-8"))
    fake_file.filename = filename
    fake_file.content_type = content_type
    return fake_file


def _post_document(client, file, authorization=None, token="internal_token"):
    data = {} if file is None else {"file": (file, file.filename)}
    headers = {}

    if token != None:
        headers["x-token"] = token

    if authorization != None:
        headers["Authorization"] = authorization

    return client.post(
        "/document-manager/document/create",
        data=data,
        headers=headers,
        content_type="multipart/form-data",
    )


def _get_document(client, document_id, user_id, token="internal_token"):
    headers = {
        "x-token": token,
        "user-id": str(user_id),
    }
    return client.get(
        f"/document-manager/document/{document_id}", headers=headers
    )


def _get_document_file(client, document_id, user_id, token="internal_token"):
    headers = {
        "x-token": token,
        "user-id": str(user_id),
    }
    return client.get(
        f"/document-manager/document/{document_id}/file", headers=headers
    )


def test_health(client):
    response = client.get("/document-manager/health")
    assert response.status_code == 200
    assert b'{"status":"up"}' in response.data


def test_create_document_without_authorization(client):
    fake_file = _create_fake_file()
    response = _post_document(client, fake_file)
    assert response.status_code == 401
    assert b"Unauthorized" in response.data


@patch("document_manager.api.documents.__validate_auth_token")
def test_create_document_without_internal_token(mock_validate_auth_token, client):
    fake_user_id = data_factory.uuid4()
    fake_authorization = data_factory.uuid4()
    mock_validate_auth_token.return_value = {
        "user_type": "ADMIN",
        "user_session_id": fake_user_id,
    }

    fake_file = _create_fake_file()
    response = _post_document(client, fake_file, fake_authorization, token=None)
    assert response.status_code == 401
    assert b"Unauthorized" in response.data


@patch("document_manager.api.documents.__validate_auth_token")
def test_create_document_bad_internal_token(mock_validate_auth_token, client):
    fake_user_id = data_factory.uuid4()
    fake_authorization = data_factory.uuid4()
    mock_validate_auth_token.return_value = {
        "user_type": "ADMIN",
        "user_session_id": fake_user_id,
    }

    fake_file = _create_fake_file()
    response = _post_document(client, fake_file, fake_authorization, token="bad_token")
    assert response.status_code == 401
    assert b"Unauthorized" in response.data


@patch("document_manager.api.documents.requests.get")
def test_create_document_auth_response_unauthorized(mock_requests_get, client):
    fake_authorization = data_factory.uuid4()

    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_requests_get.return_value = mock_response

    fake_file = _create_fake_file()
    response = _post_document(client, fake_file, fake_authorization)

    assert response.status_code == 401
    assert b"authorization required" in response.data


@patch("document_manager.api.documents.requests.get")
def test_create_document_auth_response_internal_server_error(mock_requests_get, client):
    fake_authorization = data_factory.uuid4()

    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_requests_get.return_value = mock_response

    fake_file = _create_fake_file()
    response = _post_document(client, fake_file, fake_authorization)

    assert response.status_code == 500
    assert b"internal server error on user_session_manager" in response.data


@patch("document_manager.api.documents.__validate_auth_token")
def test_create_document_success_by_seller(mock_validate_auth_token, client):
    fake_user_id = data_factory.uuid4()
    fake_authorization = data_factory.uuid4()
    mock_validate_auth_token.return_value = {
        "user_type": "SELLER",
        "user_id": fake_user_id,
    }

    fake_file = _create_fake_file()

    response = _post_document(client, fake_file, fake_authorization)

    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert "id" in response_data
    assert response_data["user_id"] == fake_user_id


@patch("document_manager.api.documents.__validate_auth_token")
def test_create_document_error_user_id_required(mock_validate_auth_token, client):
    fake_user_id = data_factory.uuid4()
    fake_authorization = data_factory.uuid4()
    mock_validate_auth_token.return_value = {
        "user_type": "SELLER",
        "user_id": None,
    }

    fake_file = _create_fake_file()

    response = _post_document(client, fake_file, fake_authorization)

    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert "message" in response_data
    assert response_data["message"] == "user-id is required"


@patch("document_manager.api.documents.__validate_auth_token")
def test_create_document_success(mock_validate_auth_token, client):
    fake_user_id = data_factory.uuid4()
    fake_authorization = data_factory.uuid4()
    mock_validate_auth_token.return_value = {
        "user_type": "ADMIN",
        "user_session_id": fake_user_id,
    }

    fake_file = _create_fake_file()

    response = _post_document(client, fake_file, fake_authorization)

    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert "id" in response_data
    assert response_data["user_id"] == fake_user_id


@patch("document_manager.api.documents.__validate_auth_token")
def test_create_document_missing_file(mock_validate_auth_token, client):
    fake_user_id = data_factory.uuid4()
    fake_authorization = data_factory.uuid4()
    mock_validate_auth_token.return_value = {
        "user_type": "ADMIN",
        "user_session_id": "12345",
    }
    response = _post_document(client, None, fake_user_id)

    assert response.status_code == 400
    assert b"No file part" in response.data


@patch("document_manager.api.documents.__validate_auth_token")
def test_create_document_invalid_file_extension(mock_validate_auth_token, client):
    fake_user_id = data_factory.uuid4()
    fake_authorization = data_factory.uuid4()
    mock_validate_auth_token.return_value = {
        "user_type": "ADMIN",
        "user_session_id": fake_user_id,
    }

    fake_file = _create_fake_file(filename="test.txt")

    response = _post_document(client, fake_file, fake_authorization)

    assert response.status_code == 400
    assert b"Invalid file extension" in response.data


@patch("document_manager.api.documents.__validate_auth_token")
def test_create_document_filename_empty(mock_validate_auth_token, client):
    fake_user_id = data_factory.uuid4()
    mock_validate_auth_token.return_value = {
        "user_type": "ADMIN",
        "user_session_id": fake_user_id,
    }

    fake_file = _create_fake_file(filename="")

    response = _post_document(client, fake_file, fake_user_id)

    assert response.status_code == 400
    assert b"No selected file" in response.data


@patch("document_manager.api.documents.__validate_auth_token")
def test_create_document_upload_error(mock_validate_auth_token, client):
    fake_user_id = data_factory.uuid4()
    fake_authorization = data_factory.uuid4()
    mock_validate_auth_token.return_value = {
        "user_type": "ADMIN",
        "user_session_id": fake_user_id,
    }

    fake_file = _create_fake_file()

    with patch(
            "document_manager.api.documents.cloud_storage_repository.upload_file",
            return_value=None,
    ):
        response = _post_document(client, fake_file, fake_authorization)

        assert response.status_code == 500
        assert b"Error uploading file" in response.data


@patch("document_manager.api.documents.__validate_auth_token")
def test_create_document_invalid_user_type(mock_validate_auth_token, client):
    fake_user_id = data_factory.uuid4()
    fake_authorization = data_factory.uuid4()
    mock_validate_auth_token.return_value = {
        "user_type": "UNKNOWN",
        "user_session_id": fake_user_id,
    }

    fake_file = _create_fake_file()

    response = _post_document(client, fake_file, fake_authorization)

    assert response.status_code == 403
    assert b"Invalid user type" in response.data


@patch("document_manager.api.documents.__validate_auth_token")
def test_get_document_by_id_success(mock_validate_auth_token, client):
    fake_user_id = data_factory.uuid4()
    fake_authorization = data_factory.uuid4()
    mock_validate_auth_token.return_value = {
        "user_type": "ADMIN",
        "user_session_id": fake_user_id,
    }
    fake_file = _create_fake_file()

    create_response = _post_document(client, fake_file, fake_authorization)
    assert create_response.status_code == 201

    response_data_create = json.loads(create_response.data)
    response = _get_document(client, response_data_create["id"], fake_user_id)

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["id"] == str(response_data_create["id"])
    assert response_data["user_id"] == str(fake_user_id)


@patch("document_manager.api.documents.__validate_auth_token")
def test_get_document_by_id_not_found(mock_validate_auth_token, client):
    fake_user_id = data_factory.uuid4()
    fake_authorization = data_factory.uuid4()
    mock_validate_auth_token.return_value = {
        "user_type": "ADMIN",
        "user_session_id": fake_user_id,
    }
    fake_document_id = data_factory.uuid4()

    response = _get_document(client, fake_document_id, fake_user_id)

    assert response.status_code == 404
    assert b"Document not found" in response.data


def test_get_document_by_id_invalid_id(client):
    fake_user_id = data_factory.uuid4()
    fake_document_id = "invalid_uuid"

    response = _get_document(client, fake_document_id, fake_user_id)

    assert response.status_code == 400
    assert b"Invalid document id" in response.data


@patch("document_manager.api.documents.__validate_auth_token")
def test_get_document_file_by_id_success(mock_validate_auth_token, client):
    fake_user_id = data_factory.uuid4()
    mock_validate_auth_token.return_value = {
        "user_type": "ADMIN",
        "user_session_id": fake_user_id,
    }
    fake_file = _create_fake_file()

    create_response = _post_document(client, fake_file, fake_user_id)
    assert create_response.status_code == 201

    response_data_create = json.loads(create_response.data)
    response = _get_document_file(client, response_data_create["id"], fake_user_id)

    assert response.status_code == 200
    print(f'response.data={response.data}')
    assert b"name,age\nJohn,30\nDoe,25" in response.data


def test_get_document_file_by_id_not_found(client):
    fake_user_id = data_factory.uuid4()
    fake_document_id = data_factory.uuid4()

    response = _get_document_file(client, fake_document_id, fake_user_id)

    assert response.status_code == 404
    assert b"Document not found" in response.data


@patch("document_manager.api.documents.__validate_auth_token")
def test_get_document_file_by_id_download_fail(mock_validate_auth_token, client):
    fake_user_id = data_factory.uuid4()
    mock_validate_auth_token.return_value = {
        "user_type": "ADMIN",
        "user_session_id": fake_user_id,
    }
    fake_file = _create_fake_file()

    create_response = _post_document(client, fake_file, fake_user_id)
    assert create_response.status_code == 201

    response_data_create = json.loads(create_response.data)

    with patch(
            "document_manager.api.documents.cloud_storage_repository.download_file",
            return_value=(None, None),
    ):
        response = _get_document_file(client, response_data_create["id"], fake_user_id)

        assert response.status_code == 409
        assert b"Download fail" in response.data
