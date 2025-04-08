import json
import os
import uuid

import requests
from flask import Blueprint, jsonify, request
from flask_validate_json import validate_json
from google.cloud import pubsub_v1
from sqlalchemy.exc import DataError
from werkzeug.exceptions import Unauthorized, InternalServerError

from ..dtos.order_in_dto import OrderInDTO
from ..dtos.order_product_in_dto import OrderProductInDTO
from ..managers.order_manager import OrderManager
from ..schemas.create_order_schema import CREATE_ORDER_SCHEMA

bp = Blueprint('orders', __name__, url_prefix='/orders')

internal_token = os.getenv('INTERNAL_TOKEN', default='internal_token')
user_session_manager_path = os.getenv('USER_SESSION_MANAGER_PATH', default='http://localhost:3008')

project_id = os.environ.get('GCP_PROJECT_ID', 'proyectofinalmiso2025')
commands_to_stock_name_pub = os.environ.get('GCP_STOCKS_TOPIC', 'commands_to_stock')

publisher_stocks = pubsub_v1.PublisherClient()
topic_path_stocks = publisher_stocks.topic_path(project_id, commands_to_stock_name_pub)

order_manager = OrderManager()


def __there_is_token() -> None:
    token = request.headers.get('x-token', None)

    if token is None:
        raise Unauthorized(description='x-token required')

    if token != internal_token:
        raise Unauthorized(description='x-token required')


def __validate_auth_token() -> dict:
    auth_token = request.headers.get('Authorization')

    auth_response = requests.get(f'{user_session_manager_path}/user_sessions/auth', headers={
        'Authorization': auth_token,
    })

    if auth_response.status_code == 401:
        raise Unauthorized(description='authorization required')
    elif auth_response.status_code != 200:
        raise InternalServerError(description='internal server error on user_session_manager')

    return auth_response.json()


def __dict_to_order_in_dto(user_id: uuid, seller_id: uuid, data: dict) -> OrderInDTO:
    return OrderInDTO(
        user_id=user_id,
        seller_id=seller_id,
        client_id=data.get('client_id'),
        delivery_date=data.get('delivery_date'),
        payment_method=data.get('payment_method'),
        products=[
            OrderProductInDTO(
                product_id=product.get('product_id'),
                units=product.get('units')
            ) for product in data.get('products', [])
        ]
    )


def __publish_order_created(order_dict: dict) -> None:
    order_id = order_dict['id']
    data = json.dumps(order_dict['products']).encode('utf-8')

    print(f"[Order Created] Publishing to {topic_path_stocks} from order_id: {order_id}, data: {data}")

    future = publisher_stocks.publish(topic_path_stocks, data)
    result = future.result()

    print(f"[Order Created] order_id: {order_id} future: {result}")


@bp.route('/create', methods=('POST',))
@validate_json(CREATE_ORDER_SCHEMA)
def create_order():
    __there_is_token()
    user_auth = __validate_auth_token()

    user_id = user_auth['user_session_id']
    seller_id = None

    request_data = request.get_json()

    if user_auth['user_type'] in ['ADMIN', 'CLIENT']:
        seller_id = request_data.get('seller_id', None)
    elif user_auth['user_type'] == 'SELLER':
        seller_id = user_auth['user_id']

    if seller_id is None:
        return jsonify({'message': 'seller_id is required'}), 400

    order_in_dto = __dict_to_order_in_dto(user_id, seller_id, request_data)
    order_created = order_manager.create_order(order_in_dto)
    __publish_order_created(order_created)

    return jsonify(order_created), 201


@bp.errorhandler(400)
@bp.errorhandler(401)
@bp.errorhandler(404)
def handle_validation_error(error):
    return jsonify({
        'message': str(error.description)
    }), error.code


@bp.errorhandler(DataError)
def handle_integrity_error(error):
    return jsonify({
        'message': f'Database integrity error. {str(error.code)}'
    }), 409
