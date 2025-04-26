# Video Manager API

Esta aplicación es un servicio para la gestión de simulaciones de video desarrollado con FastAPI y SQLAlchemy. Permite crear, consultar, actualizar y gestionar simulaciones de video almacenadas en una base de datos PostgreSQL.

## Características

- **Gestión de Simulaciones de Video:** Permite crear, consultar, actualizar y deshabilitar simulaciones de video.
- **Endpoints REST:** Proporciona endpoints para interactuar con las simulaciones de video.
- **Persistencia en PostgreSQL:** Almacena los datos de las simulaciones en una base de datos PostgreSQL.
- **Modelo Extensible:** Utiliza SQLAlchemy para definir modelos de datos flexibles y escalables.

## Requisitos

- Python 3.10
- PostgreSQL (puede ejecutarse localmente o en Docker)
- Docker (opcional, para construir la imagen de la aplicación)

## Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto (o configura las variables en tu entorno) con, al menos, las siguientes variables:

```env
# Configuración de la base de datos
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=video_manager_db
DB_TYPE=postgresql
```

## Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd video_manager_api
```

### 2. Crear y activar el entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\\Scripts\\activate
```

### 3. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación localmente

```bash
uvicorn app.main:app --reload
```

La aplicación se iniciará en `http://localhost:8000`.

## Uso de la Aplicación

### Endpoints Disponibles

#### **GET /health**
Verifica el estado de salud del servicio.

- **Respuesta exitosa (200):**
  ```json
  {
    "status": "ok"
  }
  ```

#### **POST /videos**
Crea una nueva simulación de video.

- **Cuerpo de la solicitud:**
  ```json
  {
    "document_id": "uuid-del-documento",
    "file_path": "ruta/del/archivo",
    "tags": "etiquetas, separadas, por, comas"
  }
  ```

- **Respuesta exitosa (201):**
  ```json
  {
    "id": "uuid-del-video",
    "document_id": "uuid-del-documento",
    "file_path": "ruta/del/archivo",
    "tags": "etiquetas, separadas, por, comas",
    "enabled": true,
    "update_date": "2023-01-01 12:00:00",
    "creation_date": "2023-01-01 12:00:00"
  }
  ```

#### **GET /videos/{video_id}**
Obtiene los detalles de una simulación de video específica.

- **Parámetros de ruta:**
  - `video_id` (UUID): ID del video.

- **Respuesta exitosa (200):**
  ```json
  {
    "id": "uuid-del-video",
    "document_id": "uuid-del-documento",
    "file_path": "ruta/del/archivo",
    "tags": "etiquetas, separadas, por, comas",
    "enabled": true,
    "update_date": "2023-01-01 12:00:00",
    "creation_date": "2023-01-01 12:00:00"
  }
  ```

#### **PUT /videos/{video_id}**
Actualiza los detalles de una simulación de video.

- **Parámetros de ruta:**
  - `video_id` (UUID): ID del video.

- **Cuerpo de la solicitud:**
  ```json
  {
    "file_path": "nueva/ruta/del/archivo",
    "tags": "nuevas, etiquetas",
    "enabled": false
  }
  ```

- **Respuesta exitosa (200):**
  ```json
  {
    "id": "uuid-del-video",
    "document_id": "uuid-del-documento",
    "file_path": "nueva/ruta/del/archivo",
    "tags": "nuevas, etiquetas",
    "enabled": false,
    "update_date": "2023-01-02 12:00:00",
    "creation_date": "2023-01-01 12:00:00"
  }
  ```