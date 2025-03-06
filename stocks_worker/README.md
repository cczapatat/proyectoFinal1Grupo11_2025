# Stocks Worker

Esta aplicación es un servicio de actualización de stock desarrollado con FastAPI, SQLAlchemy, Uvicorn, Redis y Google Cloud Pub/Sub. Se encarga de recibir mensajes de actualización de inventario, procesar las actualizaciones en la base de datos, actualizar la caché en Redis y despachar eventos a Pub/Sub.

## Características

- **Actualización de Stock:** Recibe comandos (lista de productos con unidades a restar) y actualiza la base de datos.
- **Validación y Registro:** Valida que el producto exista y que haya stock suficiente; registra cada intento de actualización.
- **Caché en Redis:** Actualiza la información del stock en Redis de forma asíncrona.
- **Despacho de Eventos:** Envía eventos de actualización a Google Cloud Pub/Sub.
- **Endpoints de Prueba:** Incluye endpoints para comprobar la salud del servicio, simular actualizaciones y cargar datos en bloque.

## Requisitos

- Python 3.10
- Redis (puede ejecutarse en Docker)
- PostgreSQL (puede ejecutarse localmente o en Docker)
- Google Cloud Pub/Sub (para el despacho y consumo de eventos)
- Docker (opcional, para construir la imagen de la aplicación)

## Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto (o configura las variables en tu entorno) con, al menos, las siguientes variables:

```env
# Configuración de la base de datos
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=stocks_db
DB_TYPE=postgresql

# Configuración de Google Cloud
GCP_PROJECT_ID=proyectofinalmiso2025
GCP_STOCKS_SUB=commands_to_stock-sub
GCP_STOCKS_TOPIC=commands_to_stock

# Configuración de Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
```

## Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd stocks_worker
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

- **GET /health**  
  Verifica que el servicio esté funcionando.  
  **Ejemplo de respuesta:**  
  ```json
  {"estado": "ok"}
  ```

- **POST /update_stock_test**  
  Simula una actualización de stock sin usar Pub/Sub. Se debe enviar un JSON con un arreglo de objetos que contengan `product_id` y `units`.  
  **Ejemplo de solicitud:**
  ```json
  [
    {
      "product_id": "e6da8e80-132b-4e1d-a536-6ce627c149ff",
      "units": 2
    },
    {
      "product_id": "3a195327-0b4e-4aad-a0e7-80e8dc61eee5",
      "units": 5
    }
  ]
  ```
  **Ejemplo de respuesta:**
  ```json
  {
    "mensaje": "Actualización procesada",
    "resultado": [
      {
        "product_id": "e6da8e80-132b-4e1d-a536-6ce627c149ff",
        "product_name": "Camiseta Roja",
        "last_quantity": 120,
        "new_quantity": 118,
        "status": "COMMITTED"
      },
      {
        "product_id": "3a195327-0b4e-4aad-a0e7-80e8dc61eee5",
        "product_name": "Pantalón Azul",
        "last_quantity": 80,
        "new_quantity": 75,
        "status": "COMMITTED"
      }
    ]
  }
  ```

- **POST /upload_bulk**  
  Permite cargar un archivo CSV para registrar productos en la base de datos.  
  **Formato del CSV:**  
  ```csv
  product_name,quantity_in_stock
  Camiseta Roja,120
  Pantalón Azul,80
  Zapatos Deportivos,50
  ...
  ```
  **Ejemplo de uso con cURL:**
  ```bash
  curl -X POST http://localhost:8000/upload_bulk \\
    -H "Content-Type: multipart/form-data" \\
    -F "file=@/ruta/al/archivo/bulk_products.csv"
  ```

- **POST /reset**  
  Trunca todas las tablas (stocks y update_stock_attempts) para reiniciar los datos.  
  **Ejemplo de respuesta:**
  ```json
  {"mensaje": "Tablas reseteadas exitosamente"}
  ```

## Uso con Docker

### Construir la Imagen

```bash
docker build -t stocks_worker .
```

### Ejecutar el Contenedor

```bash
docker run -d -p 8000:8000 --name stocks_worker_container stocks_worker
```

La aplicación estará disponible en `http://localhost:8000`.

## Verificación de Redis

Para comprobar las claves y sus valores en Redis, puedes utilizar el siguiente comando:

```bash
docker exec -it redis_cache redis-cli
```

Dentro del CLI de Redis, ejecuta:

- Para listar las claves:
  ```
  KEYS *
  ```
- Para obtener el valor de una clave:
  ```
  GET stock:<id_del_producto>
  ```
