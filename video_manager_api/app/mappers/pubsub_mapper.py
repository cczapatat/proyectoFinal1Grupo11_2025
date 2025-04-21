import json
from typing import List
from app.dtos.video_simulation_dto import VideoSimulationDTO


def map_pubsub_message_to_video_simulations(message: list) -> List[VideoSimulationDTO]:
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