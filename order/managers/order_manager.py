from ..dtos.order_in_dto import OrderInDTO
from ..infrastructure.order_product_repository import OrderProductRepository
from ..infrastructure.order_repository import OrderRepository


class OrderManager:
    def __init__(self):
        self.order_repository = OrderRepository()
        self.order_product_repository = OrderProductRepository()

    def create_order(self, order_in_dto: OrderInDTO) -> dict:
        order = self.order_repository.create_order(order_in_dto)
        products = self.order_product_repository.create_order_products(order.id, order_in_dto.products)

        return order.to_dict(products)
