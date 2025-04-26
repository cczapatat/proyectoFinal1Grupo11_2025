import json
from typing import List
from app.dtos.video_simulation_dto import VideoSimulationDTO


def map_pubsub_message_to_video_simulations(message: list) -> List[VideoSimulationDTO]:
    """
    Mapea una lista de mensajes de Pub/Sub a una lista de objetos VideoSimulationDTO.

    Esta función procesa cada elemento en la lista de mensajes de entrada. Si el elemento es un diccionario,
    lo convierte directamente en un objeto VideoSimulationDTO. Si el elemento es una cadena de texto, intenta
    analizarlo como JSON y, si tiene éxito, convierte el diccionario resultante en un objeto VideoSimulationDTO.
    Los elementos que no se pueden procesar son ignorados.

    Argumentos:
        message (list): Una lista de mensajes, donde cada mensaje es un diccionario o una cadena de texto
                        codificada en JSON que representa un VideoSimulationDTO.

    Retorna:
        List[VideoSimulationDTO]: Una lista de objetos VideoSimulationDTO creados a partir de los mensajes de entrada.
    """
    dtos = []
    for item in message:
        if isinstance(item, dict):
            dtos.append(VideoSimulationDTO(**item))
        elif isinstance(item, str):
            try:
                parsed = json.loads(item)
                if isinstance(parsed, dict):
                    dtos.append(VideoSimulationDTO(**parsed))
            except Exception:
                continue
    return dtos