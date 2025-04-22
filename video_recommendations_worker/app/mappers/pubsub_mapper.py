from typing import Dict, Any, List

def map_pubsub_message_to_dict(message_data: bytes) -> Dict[str, Any]:
    import json
    try:
        return json.loads(message_data.decode('utf-8'))
    except Exception as e:
        raise ValueError(f"Error parsing PubSub message: {e}")

