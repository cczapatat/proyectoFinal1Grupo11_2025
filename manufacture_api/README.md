
# Componente de Fabricas API (Manufactures)

Este componente se encarga de administrar los procesos relacionados con las fabricas.

## Índice

1. [Estructura](#estructura)
2. [Ejecución](#ejecución)
3. [Uso](#uso)
4. [Pruebas](#pruebas)
5. [Autor](#autor)

## Estructura

El proyecto está organizado de la siguiente manera:

```
.
├── manufacture_api
│   ├── src
│   │   ├── __init__.py
│   │   ├── blueprints
│   │   │   ├── __init__.py
│   │   │   └── bulk_task_blueprint.py
│   │   ├── commands
│   │   │   ├── __init__.py
│   │   │   ├── base_command.py
│   │   │   ├── create_command.py
│   │   │   ├── filter_command.py
│   │   │   ├── reset.py
│   │   │   └── update_command.py
│   │   ├── errors
│   │   │   ├── __init__.py
│   │   │   └── errors.py
│   │   ├── main.py
│   │   ├── models
│   │   │   ├── BulkTask.py
│   │   │   ├── __init__.py
│   │   ├── utilities
│   │   │   ├── __init__.py
│   │   │   └── datetime_utility.py
│   │   └── validators
│   │       ├── __init__.py
│   │       └── validators.py
            └── publisher_service.py
```

## Ejecución

### Ejecución en la Terminal

1. **Configurar la base de datos**:
   Asegúrate de tener acceso a una base de datos PostgreSQL. Si no tienes una instancia disponible, puedes ejecutar el siguiente comando para crear una:

   ```bash
   docker run --name pg2 -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=bulkTasks -p 5433:5432 -d postgres
   ```

   Alternativamente, puedes utilizar un servicio definido en el archivo `docker-compose.yml` ubicado en la raíz del proyecto. Si decides utilizar el comando anterior, asegúrate de detener el contenedor antes de ejecutar `docker-compose.yml`.

2. **Iniciar el entorno virtual de Python**:
   Es necesario tener Python 3 instalado en tu máquina.

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**:
   Modifica las variables de entorno si es necesario y luego inicia la aplicación.

   ```bash
   DB_HOST=localhost DB_PORT=5433 DB_USER=postgres DB_PASSWORD=postgres DB_NAME=bulkTasks USERS_PATH=127.0.0.1:5000 FLASK_APP=./src/main.py flask run -h 0.0.0.0 -p 5004 --debug
   ```

## Uso

Este servicio permite realizar las siguientes acciones:
- **Carga de batches para crear multiples fabricas**



## Autor

**Juan Carlos Torres Machuca**  
Correo: [jc.torresm1@uniandes.edu.co](mailto:jc.torresm1@uniandes.edu.co)
