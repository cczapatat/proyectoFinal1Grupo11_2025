import json
import os
import gc
import uuid
from google.cloud import pubsub_v1
from flask import Blueprint, jsonify, request, send_file
from werkzeug.exceptions import NotFound, BadRequest, Unauthorized

from ..dtos.order_dto import OrderDTO
from ..dtos.order_product_dto import OrderProductDTO
from ..infrastructure.order_product_repository import OrderProductRepository
from ..infrastructure.order_repository import OrderRepository

bp = Blueprint('orders', __name__, url_prefix='/orders')

internal_token = os.getenv('INTERNAL_TOKEN', default='internal_token')

order_repository = OrderRepository()
order_product_repository = OrderProductRepository()

project_id = os.environ.get('GCP_PROJECT_ID', 'proyectofinalmiso2025')
commands_to_stock_name_pub = os.environ.get('GCP_STOCKS_TOPIC', 'commands_to_stock')

publisher_stocks = pubsub_v1.PublisherClient()
topic_path_stocks = publisher_stocks.topic_path(project_id, commands_to_stock_name_pub)


def there_is_token():
    token = request.headers.get('x-token', None)

    if token is None:
        raise Unauthorized(description='authorization required')

    if token != internal_token:
        raise Unauthorized(description='authorization required')
    

def publish_order_created(order_data):
    order_id = order_data['id']
    data = json.dumps(order_data['products']).encode('utf-8')
    
    print(f"[Order Created] Publishing to {topic_path_stocks} from order_id: {order_id}, data: {data}")

    future = publisher_stocks.publish(topic_path_stocks, data)
    result = future.result()

    print(f"[Order Created] order_id: {order_id} future: {result}")


@bp.route('/create', methods=('POST',))
def create_order():
    there_is_token()
    
    data = request.get_json()

    user_id = data.get('user_id')
    products = data.get('products')

    if user_id is None:
        return jsonify({'message': 'user_id is required'}), 400
    
    if products is None:
        return jsonify({'message': 'products is required'}), 400
    
    order_dto = OrderDTO(
        user_id=user_id
    )
    order = order_repository.create_order(order_dto=order_dto)

    order_product_dtos = []
    for product in products:
        product_id = product.get('product_id')
        units = product.get('units')

        if not product_id or not units:
            return jsonify({'message': 'product_id and units are required for each product'}), 400

        order_product_dto = OrderProductDTO(
            order_id=order.id,
            product_id=product_id,
            units=units
        )
        order_product_dtos.append(order_product_dto)

    order_products = order_product_repository.create_order_products(order_product_dtos)

    response = order.to_dict()
    response['products'] = [order_product.to_dict() for order_product in order_products]

    publish_order_created(response)

    return jsonify(response), 201