import os
import uuid

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import Unauthorized, BadRequest

from ..manager.stock_manager import StockManager

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


@bp.route('/all', methods=('GET',))
def get_stocks_paginate():
    __there_is_token()

    page = max(1, request.args.get('page', default=1, type=int))
    per_page = min(max(1, request.args.get('per_page', default=10, type=int)), 50)

    return jsonify(stock_manager.get_stocks_paginate(page, per_page))


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

    return jsonify(stock_manager.get_stocks_by_ids(ids))

@bp.route('/by-store-id', methods=('GET',))
def get_stocks_by_store_id():
    __there_is_token()

    id_store = request.args.get('id_store', None)

    if id_store is None:
        return jsonify({'message': 'id_store is required'}), 400

    #transform id_store to uuid
    try:
        id_store = uuid.UUID(id_store)
    except ValueError:
        return jsonify({'message': 'invalid id_store'}), 400

    stocks_ids = stock_manager.get_stock_ids_by_store_id(id_store)

    return jsonify(stocks_ids)

@bp.route('/sync', methods=('POST',))
def sync_product_stock():
    __there_is_token()

    added_products = stock_manager.sync_products()
    
    if added_products is None:
        return jsonify({'message': 'No products were synced'}), 200
    
    return jsonify(added_products), 200


@bp.errorhandler(400)
@bp.errorhandler(401)
@bp.errorhandler(404)
def handle_validation_error(error):
    return jsonify({
        'message': str(error.description)
    }), error.code
