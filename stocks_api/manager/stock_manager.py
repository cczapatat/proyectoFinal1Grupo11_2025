import uuid

from ..infrastructure.cache_repository import CacheRepository
from ..infrastructure.stock_repository import StockRepository

stock_repository = StockRepository()
cache_repository = CacheRepository()


def get_stocks_paginate_from_cache(page: int, per_page: int):
    cache_key = f'stocks_paginate:{page}_{per_page}'
    stocks_cached = cache_repository.get(cache_key)

    return stocks_cached


def set_cache_stocks_paginate(page: int, per_page: int, stocks: list):
    if len(stocks) > 0:
        cache_key = f'stocks_paginate:{page}_{per_page}'
        cache_repository.set(cache_key, stocks)


def sync_quantity_in_stock(stocks: list, page: int, per_page: int):
    if len(stocks) > 0:
        need_old_keys = False
        stocks_id = [f"stock:{stock['id']}" for stock in stocks]
        stocks_update = cache_repository.get_multiple(stocks_id)

        if len(stocks_update) > 0:
            need_old_keys = True
            stocks_update_dict = {stock['id']: stock['quantity_in_stock'] for stock in stocks_update}
            for stock in stocks:
                if stock['id'] in stocks_update_dict:
                    stock['quantity_in_stock'] = stocks_update_dict[stock['id']]

        if need_old_keys:
            stocks_id_to_delete = [f"stock:{stock['id']}" for stock in stocks_update]
            cache_repository.delete(f'stocks_paginate:{page}_{per_page}')
            cache_repository.delete_multiple(stocks_id_to_delete)


class StockManager:
    @staticmethod
    def get_stocks_paginate(page: int, per_page: int):
        cached_stocks = get_stocks_paginate_from_cache(page, per_page)
        if cached_stocks is not None:
            sync_quantity_in_stock(cached_stocks, page, per_page)
            return cached_stocks

        stocks = stock_repository.get_documents(page=page, per_page=per_page)
        stocks_dict = [stock.to_dict() for stock in stocks]

        set_cache_stocks_paginate(page, per_page, stocks_dict)

        return stocks_dict

    @staticmethod
    def get_stocks_by_ids(ids: list[uuid.uuid4]) -> list[dict]:
        stocks = stock_repository.get_documents_by_ids(ids)
        stocks_dict = [stock.to_dict() for stock in stocks]

        return stocks_dict
