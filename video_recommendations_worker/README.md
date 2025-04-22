# Trabajador de Recomendaciones de Video

Un servicio que consume eventos de simulación de video desde Google Cloud Pub/Sub y genera recomendaciones minoristas impulsadas por IA utilizando OpenAI y Semantic Kernel.

## Resumen de la Arquitectura

Este proyecto es parte de una arquitectura de microservicios que consta de:

1. **API del Gestor de Videos**: Maneja los endpoints de la API para la gestión de simulaciones de video y publica eventos en Pub/Sub.
2. **Trabajador de Recomendaciones de Video (este proyecto)**: Consume eventos de simulación de video y genera recomendaciones impulsadas por IA.

## Funcionalidad del Trabajador

Este servicio:

1. Se suscribe al tema `video_to_simulation` de Pub/Sub.
2. Recibe mensajes cuando se crean o actualizan nuevas simulaciones de video.
3. Extrae las etiquetas del video (por ejemplo, "productos agotados").
4. Utiliza OpenAI y Semantic Kernel para generar recomendaciones minoristas accionables.
5. Almacena las recomendaciones en la base de datos para su posterior recuperación.

## Generación de Recomendaciones con IA

El sistema de recomendaciones:

1. Utiliza un pipeline de Semantic Kernel con integración de OpenAI.
2. Analiza las etiquetas de los videos para comprender los problemas minoristas.
3. Genera de 3 a 5 recomendaciones específicas y accionables para los gerentes de tienda.
4. Se enfoca en soluciones prácticas a los problemas identificados.
5. Formatea las recomendaciones como puntos concisos.

### Ejemplo de Recomendaciones

Para un video etiquetado como "productos agotados, estantes vacíos":

```
- Reabastecer los artículos de alta demanda de inmediato para evitar la frustración de los clientes.
- Implementar alertas automáticas de inventario cuando los niveles de stock alcancen umbrales críticos.
- Crear relaciones con proveedores de respaldo para los artículos que frecuentemente se agotan.
- Capacitar al personal en procedimientos adecuados de gestión de inventario.
- Mostrar fechas esperadas de reabastecimiento para los artículos agotados para mantener la confianza del cliente.
```

## Variables de Entorno

Cree un archivo `.env` con las siguientes variables:

```
# Conexión a la Base de Datos
DB_USER=user_final
DB_PASSWORD=pass_final
DB_HOST=localhost
DB_PORT=5432
DB_NAME=project_final
DB_TYPE=postgresql

# Google Cloud PubSub
GCP_PROJECT_ID=proyectofinalmiso2025
GCP_VIDEO_SIMULATION_SUB=video_to_simulation-sub

# Configuración de OpenAI
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=500
OPENAI_TOP_P=0.95
```

## Configuración e Instalación

1. Cree un entorno virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. Instale las dependencias:
   ```
   pip install -r requirements.txt
   ```

3. Configure las variables de entorno (vea la sección anterior).

4. Ejecute el trabajador:
   ```
   python main.py
   ```

## Pruebas

Para ejecutar las pruebas de integración:

```
python -m unittest tests/integration_test.py
```

Las pruebas utilizan mocks para las operaciones de base de datos, Pub/Sub y llamadas a la API de OpenAI por defecto. Para pruebas de extremo a extremo con la API del Gestor de Videos y llamadas reales a OpenAI, configure la variable de entorno `RUN_E2E_TESTS`:

```
export RUN_E2E_TESTS=1
python -m unittest tests/integration_test.py
```

## Interacción con la API del Gestor de Videos

Este servicio consume mensajes publicados por la API del Gestor de Videos. Para crear un flujo de trabajo completo:

1. Use la API del Gestor de Videos para crear o actualizar simulaciones de video.
2. La API publicará mensajes en Pub/Sub.
3. Este trabajador consumirá esos mensajes.
4. Se generarán y almacenarán recomendaciones impulsadas por IA.
5. Las recomendaciones se pueden recuperar a través de una API separada (no implementada en este proyecto).

## Esquema de la Base de Datos

El servicio utiliza una base de datos PostgreSQL con la siguiente tabla:

```sql
CREATE TABLE video_recommendations (
    id UUID PRIMARY KEY,
    video_simulation_id UUID NOT NULL,
    document_id UUID NOT NULL,
    recommendations TEXT NOT NULL,
    update_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    creation_date TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```
