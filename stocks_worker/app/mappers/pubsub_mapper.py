import json
from typing import List
from app.dtos.product_update_dto import ProductUpdateDTO

def map_pubsub_message_to_product_updates(message: list) -> List[ProductUpdateDTO]:
    dtos = []
    for item in message:
        if isinstance(item, dict):
            dtos.append(ProductUpdateDTO(**item))
        elif isinstance(item, str):
            # No tener en cuenta los encabezados
            if item.strip().lower() in ["id", "product_id", "units"]:
                continue
            try:
                parsed = json.loads(item)
                if isinstance(parsed, dict):
                    dtos.append(ProductUpdateDTO(**parsed))
            except Exception:
                continue
    return dtos