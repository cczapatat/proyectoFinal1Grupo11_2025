
from ..dtos.store_x_products_dto import ProductStockDTO, StoreXProductsDTO


class EntityMapper:
    @staticmethod
    def json_to_dto(json_data: dict) -> StoreXProductsDTO:
        store_id = json_data.get('store_id')
        stocks = json_data.get('stocks')

        if not stocks:
            return StoreXProductsDTO(id_store=store_id, stocks=[])

        product_stocks = []
        for stock in stocks:
            product_stock = ProductStockDTO(
                id=stock.get('id'),
                id_product=stock.get('product_id'),
                assigned_stock=stock.get('assigned_stock')
            )
            product_stocks.append(product_stock)

        return StoreXProductsDTO(id_store=store_id, stocks=product_stocks)
    