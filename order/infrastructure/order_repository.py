import uuid
from datetime import datetime

from ..config.db import db
from ..dtos.order_in_dto import OrderInDTO
from ..models.enums import ORDER_STATE
from ..models.order_model import Order


class OrderRepository:

    @staticmethod
    def create_order(order_id: uuid, total_amount: float, order_dto: OrderInDTO) -> Order:
        order = Order()
        order.id = order_id,
        order.user_id = order_dto.user_id
        order.seller_id = order_dto.seller_id
        order.client_id = order_dto.client_id
        order.delivery_date = order_dto.delivery_date
        order.payment_method = order_dto.payment_method
        order.total_amount = total_amount
        order.state = ORDER_STATE.CREATED
        order.created_at = datetime.now()
        order.updated_at = datetime.now()

        db.session.add(order)
        return order
