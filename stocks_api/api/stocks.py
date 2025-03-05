import os
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import Unauthorized

from ..manager.stock_manager import StockManager

bp = Blueprint('stocks', __name__, url_prefix='/stocks-api/stocks')

internal_token = os.getenv('INTERNAL_TOKEN', default='internal_token')

stock_manager = StockManager()

def there_is_token():
    token = request.headers.get('x-token', None)

    if token is None:
        raise Unauthorized(description='authorization required')

    if token != internal_token:
        raise Unauthorized(description='authorization required')


@bp.route('/all', methods=('GET',))
def get_stocks_paginate():
    there_is_token()

    page = max(1, request.args.get('page', default=1, type=int))
    per_page = min(max(1, request.args.get('per_page', default=10, type=int)), 50)

    return jsonify(stock_manager.get_stocks_paginate(page, per_page))
