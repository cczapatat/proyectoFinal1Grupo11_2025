import json

from ..config.cache import cache

class CacheRepository:
    @staticmethod
    def get(key: str):
        data = cache.get(key)
        if data:
            return json.loads(data)
        return None

    @staticmethod
    def set(key: str, value, timeout: int = 300) -> None:
        cache.set(key, json.dumps(value), ex=timeout)