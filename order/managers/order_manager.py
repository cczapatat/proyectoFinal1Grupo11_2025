import uuid

from ..dtos.order_in_dto import OrderInDTO
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
        def transaction_operations() -> [Order, OrderProduct]:
            order_id = uuid.uuid4()
            order_internal = self.order_repository.create_order(order_id, order_in_dto)
            products_internal = self.order_product_repository.create_order_products(order_id, order_in_dto.products)
            return [order_internal, products_internal]

        [order, products] = self.transaction.run(transaction_operations)

        return order.to_dict(products)
