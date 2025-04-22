from openai import OpenAI
import logging
from typing import Dict, Any
from app.ai.configuration import OpenAIConfig
from app.ai.recommendation_agents import RecommendationAgentInstructions

class RecommendationsHandler:
    """
    Maneja la generación de recomendaciones basadas en IA para videos basados en etiquetas.
    Utiliza la API de OpenAI para analizar etiquetas y generar recomendaciones apropiadas.
    """
    
    def __init__(self) -> None:
        """Inicializa el RecommendationsHandler con la configuración de OpenAI."""
        OpenAIConfig.validate_config()
        
        # Inicializa el cliente de OpenAI
        self.client = OpenAI(api_key=OpenAIConfig.API_KEY)
        
        # Almacena la plantilla del prompt para uso posterior
        self.prompt_template = RecommendationAgentInstructions.TAG_ANALYSIS_PROMPT
        
        # Almacena los parámetros de configuración
        self.config: Dict[str, Any] = {
            "model": OpenAIConfig.MODEL,
            "temperature": OpenAIConfig.TEMPERATURE,
            "max_tokens": OpenAIConfig.MAX_TOKENS,
            "top_p": OpenAIConfig.TOP_P
        }
        
        logging.info(f"RecommendationsHandler inicializado con el modelo {OpenAIConfig.MODEL}")

    async def generate_recommendations(self, tags: str) -> str:
        """
        Genera recomendaciones utilizando la finalización de OpenAI basada en las etiquetas proporcionadas.
        
        Args:
            tags: Las etiquetas a analizar
            
        Returns:
            str: Recomendaciones generadas como una cadena de texto
            
        Raises:
            Exception: Si ocurre un error al llamar a la API de OpenAI
        """
        try:
            # Formatea el prompt con la etiqueta
            formatted_prompt = self.prompt_template.format(tag=tags)
            print(f"Prompt formateado: {formatted_prompt}")
            
            # Llama a OpenAI con la nueva API basada en cliente
            response = self.client.chat.completions.create(
                model=self.config["model"],
                messages=[
                    {"role": "system", "content": "Eres un asistente de IA que analiza etiquetas de videos y genera recomendaciones."},
                    {"role": "user", "content": formatted_prompt}
                ],
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"],
                top_p=self.config["top_p"]
            )
            
            # Extrae el contenido de la respuesta utilizando la nueva estructura de la API
            result = response.choices[0].message.content
            
            return result
        except Exception as e:
            logging.error(f"Error al llamar a OpenAI: {e}")
            raise
