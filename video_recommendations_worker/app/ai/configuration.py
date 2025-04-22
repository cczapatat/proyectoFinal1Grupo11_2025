import os
from dotenv import load_dotenv

load_dotenv()

class OpenAIConfig:
    """
    OpenAIConfig es una clase de configuración para gestionar los ajustes de la API de OpenAI.
    Atributos:
        API_KEY (str): Clave API para autenticación, se recomienda configurarla a través de 
            la variable de entorno "OPENAI_API_KEY" por seguridad.
        MODEL (str): Modelo de OpenAI a utilizar, el valor predeterminado es "gpt-4o", configurable 
            mediante "OPENAI_MODEL".
        TEMPERATURE (float): Controla la aleatoriedad en la salida, el valor predeterminado es 0.7.
        MAX_TOKENS (int): Máximo número de tokens en la respuesta, el valor predeterminado es 500.
        TOP_P (float): Controla el muestreo por núcleo, el valor predeterminado es 0.95.
    Métodos:
        validate_config(): Verifica que API_KEY esté configurada, lanza ValueError si falta.
    Uso:
        - Configura las variables de entorno necesarias (por ejemplo, "OPENAI_API_KEY") antes de ejecutar.
        - Usa los valores predeterminados o sobrescríbelos mediante variables de entorno según sea necesario.
        - Llama a `validate_config` para verificar la configuración antes de realizar solicitudes a la API.
    """
    API_KEY = os.getenv("OPENAI_API_KEY", "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")
    MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    # Model parameters
    TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "500"))
    TOP_P = float(os.getenv("OPENAI_TOP_P", "0.95"))
    
    @staticmethod
    def validate_config():
        if not OpenAIConfig.API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

