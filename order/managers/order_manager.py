import uuid

from werkzeug.exceptions import BadRequest

from ..dtos.order_in_dto import OrderInDTO
from ..http_services.users_http import get_seller_by_id, get_client_by_id, get_product_stocks_by_id
from ..infrastructure.order_product_repository import OrderProductRepository
from ..infrastructure.order_repository import OrderRepository
from ..infrastructure.transaction import Transaction
from ..models.order_model import Order
from ..models.order_product_model import OrderProduct


class OrderManager:
    def __init__(self):
        self.order_repository = OrderRepository()
        self.order_product_repository = OrderProductRepository()
        self.transaction = Transaction()

    def create_order(self, order_in_dto: OrderInDTO) -> dict:
        get_seller_by_id(order_in_dto.seller_id)
        get_client_by_id(order_in_dto.client_id, order_in_dto.seller_id)

        product_stocks_id = [product.product_id for product in order_in_dto.products]
        product_stocks = get_product_stocks_by_id(product_stocks_id)

        if len(product_stocks) != len(order_in_dto.products):
            raise BadRequest(description='product stocks not found')

        total_order_value = 0.0
        for product in order_in_dto.products:
            product_on_stock = next((p for p in product_stocks if p['id'] == product.product_id), None)
            if product_on_stock is None or (product_on_stock['quantity_in_stock'] - product.units) < 0:
                raise BadRequest(description=f'not enough product stocks {product.product_id}')
            total_order_value += float(product_on_stock['product'].get('unit_price', 0.0)) * product.units

        def transaction_operations() -> [Order, OrderProduct]:
            order_id = uuid.uuid4()
            order_internal = self.order_repository.create_order(order_id, float(total_order_value), order_in_dto)
            products_internal = self.order_product_repository.create_order_products(order_id, order_in_dto.products)
            return [order_internal, products_internal]

        [order, products] = self.transaction.run(transaction_operations)

        return order.to_dict(products)
