import uuid

from ..dtos.store_x_products_dto import StoreXProductsDTO
from ..http_services.products_http import get_products_by_id
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


def populate_products(stocks: list):
    if len(stocks) > 0:
        products_id = [stock['id_product'] for stock in stocks]
        products = get_products_by_id(products_id)
        products_dict = {product['id']: product for product in products}

        for stock in stocks:
            if stock['id_product'] in products_dict:
                stock['product'] = products_dict[stock['id_product']]
            else:
                stock['product'] = {}


class StockManager:
    @staticmethod
    def get_stocks_paginate(page: int, per_page: int) -> [list[dict], int]:
        cached_stocks = get_stocks_paginate_from_cache(page, per_page)
        if cached_stocks is not None:
            sync_quantity_in_stock(cached_stocks, page, per_page)
            populate_products(cached_stocks)
            stocks_dict = cached_stocks
        else:
            stocks = stock_repository.get_documents(page=page, per_page=per_page)
            stocks_dict = [stock.to_dict() for stock in stocks]
            set_cache_stocks_paginate(page, per_page, stocks_dict)
            populate_products(stocks_dict)

        total_stocks = stock_repository.get_total_documents()
        return [stocks_dict, total_stocks]

    @staticmethod
    def get_stocks_by_ids(ids: list[uuid.uuid4]) -> list[dict]:
        stocks = stock_repository.get_documents_by_ids(ids)
        stocks_dict = [stock.to_dict() for stock in stocks]
        populate_products(stocks_dict)

        return stocks_dict

    @staticmethod
    def get_stocks_by_store_id(id_store: uuid.uuid4) -> list[StoreXProductsDTO]:
        stocks = stock_repository.get_stocks_by_store_id(id_store)
        if stocks is None:
            return []
        return stocks

    @staticmethod
    def assign_stock_store(store_x_products_dto: StoreXProductsDTO):

        store_id = store_x_products_dto.id_store
        stocks = store_x_products_dto.stocks

        if not stocks:
            return {'message': 'No products to assign'}

        for stock in stocks:
            if stock.id_product is '' or stock.assigned_stock is '':
                return {'message': 'Error: Invalid product or stock data'}
            stock_repository.assign_stock_to_store(stock.id, store_id, stock.id_product, stock.assigned_stock)

        # Clear the cache for the specific stock
        for stock in stocks:
            cache_key = f'stock:{stock.id_product}'
            cache_repository.delete(cache_key)

        return {'message': 'Stocks assigned successfully'}
