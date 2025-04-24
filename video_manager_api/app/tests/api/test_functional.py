import json
import uuid
from datetime import datetime

class TestVideoSimulationAPI:
    def test_health_check(self, client):
        """
        Prueba el endpoint de verificación de salud.
        """
        response = client.get("/video/health")
        assert response.status_code == 200
        assert response.json() == {"estado": "ok"}

    def test_create_video_simulation(self, client):
        """
        Prueba la creación de una simulación de video.
        """
        payload = {
            "document_id": str(uuid.uuid4()),
            "store_id": str(uuid.uuid4()),
            "file_path": "/test/sample_video.mp4",
            "tags": "trafico de clientes bajo durante la hora del almuerzo",
            "enabled": True
        }
        response = client.post("/video/create", json=payload)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["mensaje"] == "Información de video cargada correctamente"
        assert "resultado" in response_data
        assert response_data["resultado"]["document_id"] == payload["document_id"]
        assert response_data["resultado"]["file_path"] == payload["file_path"]
        assert response_data["resultado"]["tags"] == payload["tags"]
        assert response_data["resultado"]["enabled"] == payload["enabled"]

    def test_create_video_simulation_invalid(self, client):
        """
        Prueba la creación de una simulación de video con datos inválidos.
        """
        payload = {
            "document_id": '',
            "store_id": str(uuid.uuid4()),
            "file_path": "/test/sample_video.mp4",
            "tags": "trafico de clientes bajo durante la hora del almuerzo",
            "enabled": True
        }
        # Simular un error en la creación
        response = client.post("/video/create", json=payload)
        assert response.status_code == 422

    def test_get_all_video_simulations(self, client):
        """
        Prueba la obtención de todas las simulaciones de video.
        """
        response = client.get("/video/get_all")
        assert response.status_code == 200
        response_data = response.json()
        assert "mensaje" in response_data
        assert "cantidad" in response_data
        assert "videos" in response_data
        assert isinstance(response_data["videos"], list)

    def test_get_video_simulation_by_id(self, client):
        """
        Prueba la obtención de una simulación de video por su ID.
        """
        # Crear una simulación de video para probar
        payload = {
            "document_id": str(uuid.uuid4()),
            "store_id": str(uuid.uuid4()),
            "file_path": "/test/sample_video.mp4",
            "tags": "test,sample",
            "enabled": True
        }
        create_response = client.post("/video/create", json=payload)
        assert create_response.status_code == 200
        created_video = create_response.json()["resultado"]

        # Obtener la simulación creada por ID
        response = client.get(f"/video/get_by_id?video_simulation_id={created_video['id']}")
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["id"] == created_video["id"]
        assert response_data["document_id"] == created_video["document_id"]
        assert response_data["file_path"] == created_video["file_path"]
        assert response_data["tags"] == created_video["tags"]
        assert response_data["enabled"] == created_video["enabled"]

    def test_get_video_simulation_by_id_not_found(self, client):
        """
        Prueba la obtención de una simulación de video que no existe.
        """
        non_existent_id = str(uuid.uuid4())
        response = client.get(f"/video/get_by_id?video_simulation_id={non_existent_id}")
        assert response.status_code == 400
        assert "Error" in response.json()["detail"]
    
    def test_get_video_simulation_by_id_invalid(self, client):
        """
        Prueba la obtención de una simulación de video con un ID inválido.
        """
        invalid_id = "invalid_id"
        response = client.get(f"/video/get_by_id?video_simulation_id={invalid_id}")
        assert response.status_code == 400

    from unittest.mock import patch

    @patch("app.repositories.video_simulation_repository.dispatch_video_simulation_event")
    @patch("app.repositories.video_simulation_repository.pubsub_publisher_available", True)
    def test_create_video_simulation_pubsub(self, mock_dispatch_event, client):
        """
        Prueba la creación de una simulación de video y verifica que se publique un evento en Pub/Sub.
        """
        payload = {
            "document_id": str(uuid.uuid4()),
            "store_id": str(uuid.uuid4()),
            "file_path": "/test/sample_video.mp4",
            "tags": "trafico de clientes bajo durante la hora del almuerzo",
            "enabled": True
        }

        # Enviar la solicitud para crear la simulación de video
        response = client.post("/video/create", json=payload)
        assert response.status_code == 200

        # Verificar que se haya llamado a la función de publicación en Pub/Sub
        assert mock_dispatch_event.called
        mock_dispatch_event.assert_called_once()

        # Verificar los argumentos con los que se llamó a la función
        called_args = mock_dispatch_event.call_args[0]
        assert called_args[1] == payload["document_id"]  # document_id
        assert called_args[2] == payload["file_path"]    # file_path
        assert called_args[3] == payload["enabled"]      # enabled
        assert called_args[4] == payload["tags"]         # tags

    @patch("app.repositories.video_simulation_repository.pubsub_publisher_available", False)
    def test_create_video_simulation_no_pubsub(self, client, caplog):
        """
        Prueba la creación de una simulación de video cuando Pub/Sub no está disponible.
        """
        payload = {
            "document_id": str(uuid.uuid4()),
            "store_id": str(uuid.uuid4()),
            "file_path": "/test/sample_video.mp4",
            "tags": "trafico de clientes bajo durante la hora del almuerzo",
            "enabled": True
        }

        # Enviar la solicitud para crear la simulación de video
        response = client.post("/video/create", json=payload)
        assert response.status_code == 200