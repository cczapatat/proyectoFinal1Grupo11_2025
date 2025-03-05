from datetime import datetime

from ..config.db import db
from ..models.order_product_model import OrderProduct
from ..dtos.order_product_dto import OrderProductDTO


class OrderProductRepository:

    @staticmethod
    def create_order_products(order_product_dtos: list[OrderProductDTO]) -> list[OrderProduct]:
        order_products = []

        for order_product_dto in order_product_dtos:
            order_product = OrderProduct()
            order_product.order_id = order_product_dto.order_id
            order_product.product_id = order_product_dto.product_id
            order_product.units = order_product_dto.units
            order_product.created_at = datetime.now()
            order_product.updated_at = datetime.now()

            db.session.add(order_product)
            order_products.append(order_product)

        db.session.commit()

        return order_products
