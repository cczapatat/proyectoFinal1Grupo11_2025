import json

from ..config.cache import cache


class CacheRepository:

    @staticmethod
    def get_multiple(keys: list[str]) -> list:
        data = cache.mget(keys)
        return [json.loads(item) for item in data if item is not None]

    @staticmethod
    def set(key: str, value, timeout: int = 300) -> None:
        cache.set(key, json.dumps(value), ex=timeout)

    @staticmethod
    def delete(key: str) -> None:
        cache.delete(key)
