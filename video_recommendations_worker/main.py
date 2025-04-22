import logging
import asyncio
import signal
from app.pubsub.consumer import consume_messages
from app.core.db import create_tables
from app.ai.configuration import OpenAIConfig

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def handle_shutdown(signum, frame):
    """Manejo el desconexion de la aplicación"""
    logger.info("Señal de desconexion recibida. Cerrando...")
    exit(0)

def main():
    """Punto de entrada principal de la aplicación"""
    # Configurar manejadores de apagado
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    
    logger.info("Iniciando el Worker de Recomendaciones de Video")
    
    try:
        # Validar configuración de OpenAI
        OpenAIConfig.validate_config()
        logger.info("Configuración de OpenAI validada")
        
        # Crear tablas de la base de datos si no existen
        create_tables()
        logger.info("Tablas de la base de datos creadas")
        
        # Iniciar consumo de mensajes
        logger.info("Iniciando el consumidor de PubSub...")
        consume_messages()
        
    except ValueError as e:
        logger.error(f"Error de configuración: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"Error al iniciar el worker: {e}")
        exit(1)

if __name__ == "__main__":
    main()
