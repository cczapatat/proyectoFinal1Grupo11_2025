import os
import json
import redis

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_DB = int(os.environ.get("REDIS_DB", 0))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)

def update_stock_cache(stock_id: str, quantity_in_stock: int):
    key = f"stock:{stock_id}"
    data = {"id": stock_id, "quantity_in_stock": quantity_in_stock}
    redis_client.set(key, json.dumps(data))
    print(f"Actualizado en redis caché: {key} -> {data}")