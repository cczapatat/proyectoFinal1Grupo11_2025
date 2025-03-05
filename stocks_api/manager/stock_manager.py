from ..infrastructure.stock_repository import StockRepository
from ..infrastructure.cache_repository import CacheRepository

stock_repository = StockRepository()
cache_repository = CacheRepository()


class StockManager:
    @staticmethod
    def get_stocks_paginate(page: int, per_page: int):
        cache_key = f'stocks_paginate:{page}_{per_page}'

        cached_stocks = cache_repository.get(cache_key)
        if cached_stocks is not None:
            return cached_stocks

        stocks = stock_repository.get_documents(page=page, per_page=per_page)
        stocks_dict = [stock.to_dict() for stock in stocks]

        if len(stocks_dict) > 0:
            cache_repository.set(cache_key, stocks_dict)

        return stocks_dict
