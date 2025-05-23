import os
import uuid

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import Unauthorized, BadRequest

from ..manager.stock_manager import StockManager
from ..mapper.entity_to_dto import EntityMapper

bp = Blueprint('stocks', __name__, url_prefix='/stocks-api/stocks')

internal_token = os.getenv('INTERNAL_TOKEN', default='internal_token')

stock_manager = StockManager()


def __there_is_token():
    token = request.headers.get('x-token', None)

    if token is None:
        raise Unauthorized(description='authorization required')

    if token != internal_token:
        raise Unauthorized(description='authorization required')


def __valid_uuid(uuid_string: str) -> uuid.uuid4:
    try:
        uuid.UUID(uuid_string)
    except ValueError:
        raise BadRequest(description='invalids product ids')


@bp.route('/assign-stock-store', methods=('PUT',))
def assign_stock_store():
    __there_is_token()

    data = request.get_json()

    if data is None:
        return jsonify({'message': 'data is required'}), 400

    store_x_products_dto = EntityMapper.json_to_dto(data)

    if store_x_products_dto is None:
        return jsonify({'message': 'invalid data'}), 400

    result = stock_manager.assign_stock_store(store_x_products_dto)

    if result["message"].__contains__("Error"):
        return jsonify(result), 400

    return jsonify(result), 200


@bp.route('/all', methods=('GET',))
def get_stocks_paginate():
    __there_is_token()

    page = max(1, request.args.get('page', default=1, type=int))
    per_page = min(max(1, request.args.get('per_page', default=10, type=int)), 50)
    [stocks, total] = stock_manager.get_stocks_paginate(page=page, per_page=per_page)

    return jsonify({'stocks': stocks, 'total': total, 'page': page, 'per_page': per_page}), 200


@bp.route('/list-all', methods=('GET',))
def get_stocks_list_all():
    __there_is_token()
    stocks = stock_manager.get_stocks()

    return jsonify(stocks), 200


@bp.route('/by-ids', methods=('POST',))
def get_stocks_by_ids():
    __there_is_token()

    ids = request.get_json().get('ids', None)

    if ids is None:
        return jsonify({'message': 'ids is required'}), 400

    if not isinstance(ids, list):
        return jsonify({'message': 'ids must be a list'}), 400

    if len(ids) == 0:
        return jsonify({'message': 'ids cannot be empty'}), 400

    for id in ids:
        __valid_uuid(id)

    return jsonify(stock_manager.get_stocks_by_ids(ids)), 200


@bp.route('/by-store-id', methods=('GET',))
def get_stocks_by_store_id():
    __there_is_token()

    id_store = request.args.get('id_store', None)

    if not id_store:
        return jsonify({'message': 'id_store is required'}), 400

    try:
        id_store = uuid.UUID(id_store)
    except ValueError:
        return jsonify({'message': 'invalid id_store'}), 400

    stocks = stock_manager.get_stocks_by_store_id(id_store)

    if stocks is None:
        return jsonify({'message': 'store not found'}), 404

    if not stocks.stocks:
        return jsonify({'message': 'store without stocks'}), 200

    return jsonify(stocks.to_dict()), 200

@bp.route('/product_and_store', methods=('GET',))
def get_stocks_by_product_id_and_store_id():
    __there_is_token()

    id_store = request.args.get('id_store', None)
    id_product = request.args.get('id_product', None)

    if not id_store:
        return jsonify({'message': 'id_store is required'}), 400

    if not id_product:
        return jsonify({'message': 'id_product is required'}), 400

    try:
        id_product = uuid.UUID(id_product)
    except ValueError:
        return jsonify({'message': 'invalid id_product'}), 400
    try:
        id_store = uuid.UUID(id_store)
    except ValueError:
        return jsonify({'message': 'invalid id_store'}), 400

    stock = stock_manager.get_stocks_by_product_id_and_store_id(id_product, id_store)
    if stock is None:
        return jsonify({'message': 'stock not found'}), 404

    if not stock.get("product"):
        return jsonify({'message': 'stock not found'}), 404

    return jsonify(stock), 200

@bp.errorhandler(400)
@bp.errorhandler(401)
@bp.errorhandler(404)
def handle_validation_error(error):
    return jsonify({
        'message': str(error.description)
    }), error.code
