from datetime import datetime

from ..config.db import db
from ..models.order_model import Order
from ..dtos.order_dto import OrderDTO


class OrderRepository:

    @staticmethod
    def create_order(order_dto: OrderDTO) -> Order:
        order = Order()
        order.user_id = order_dto.user_id
        order.state = 'created'
        order.created_at = datetime.now()
        order.updated_at = datetime.now()

        db.session.add(order)
        db.session.commit()

        return order
