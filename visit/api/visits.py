import os
import uuid
from datetime import datetime

import requests
from flask import Blueprint, jsonify, request
from flask_validate_json import validate_json
from sqlalchemy.exc import DataError
from werkzeug.exceptions import Unauthorized, InternalServerError

from ..dtos.visit_in_dto import VisitInDTO
from ..dtos.visit_product_in_dto import VisitProductInDTO
from ..managers.visit_manager import VisitManager
from ..schemas.create_visit_schema import CREATE_VISIT_SCHEMA

bp = Blueprint('visits', __name__, url_prefix='/visits')

internal_token = os.getenv('INTERNAL_TOKEN', default='internal_token')
user_session_manager_path = os.getenv('USER_SESSION_MANAGER_PATH', default='http://localhost:3008')

visit_manager = VisitManager()


def __there_is_token() -> None:
    token = request.headers.get('x-token', None)

    if token is None:
        raise Unauthorized(description='x-token required')

    if token != internal_token:
        raise Unauthorized(description='x-token required')


def __validate_auth_token() -> dict:
    auth_token = request.headers.get('Authorization', None)

    if auth_token is None:
        raise Unauthorized(description='authorization required')

    auth_response = requests.get(f'{user_session_manager_path}/user_sessions/auth', headers={
        'Authorization': auth_token,
    })

    if auth_response.status_code == 401:
        raise Unauthorized(description='authorization required')
    elif auth_response.status_code != 200:
        raise InternalServerError(description='internal server error on user_session_manager')

    return auth_response.json()


def __dict_to_visit_in_dto(user_id: uuid, seller_id: uuid, data: dict) -> VisitInDTO:
    return VisitInDTO(
        user_id=user_id,
        seller_id=seller_id,
        client_id=data.get('client_id'),
        description=data.get('description'),
        visit_date=data.get('visit_date'),
        products=[
            VisitProductInDTO(
                product_id=product.get('product_id'),
            ) for product in data.get('products', [])
        ]
    )


@bp.route('/create', methods=('POST',))
@validate_json(CREATE_VISIT_SCHEMA)
def create_order():
    __there_is_token()
    user_auth = __validate_auth_token()

    user_id = user_auth['user_session_id']

    if user_auth['user_type'] != 'SELLER':
        raise Unauthorized(description='un authorization operation')

    seller_id = user_auth['user_id']

    if seller_id is None:
        return jsonify({'message': 'seller_id is required'}), 400

    request_data = request.get_json()

    visit_in_dto = __dict_to_visit_in_dto(user_id, seller_id, request_data)
    visit_created = visit_manager.create_visit(visit_in_dto)

    return jsonify(visit_created), 201

@bp.route('/by-visit-date/<string:visit_date>', methods=('GET',))
def get_all_visits_by_visit_date(visit_date: str):
    __there_is_token()
    user_auth = __validate_auth_token()

    if user_auth['user_type'] != 'SELLER':
        raise Unauthorized(description='un authorization operation')

    seller_id = user_auth['user_id']

    if seller_id is None:
        return jsonify({'message': 'seller_id is required'}), 400

    try:
        # Ensure visit_date is parsed correctly
        parsed_date = datetime.strptime(visit_date, '%Y-%m-%d').date()
        visits = visit_manager.get_all_visits_by_visit_date(parsed_date)
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    return jsonify(visits), 200

@bp.route('/by-visit-date-paginated/<string:visit_date>', methods=('GET',))
def get_all_visits_by_visit_date_paginated(visit_date: str):
    __there_is_token()
    user_auth = __validate_auth_token()

    if user_auth['user_type'] != 'SELLER':
        raise Unauthorized(description='unauthorized operation')

    seller_id = user_auth['user_id']

    if seller_id is None:
        return jsonify({'message': 'seller_id is required'}), 400

    try:
        # Parse query parameters with defaults
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        sort_order = request.args.get('sort_order', 'asc').lower()

        # Ensure visit_date is parsed correctly
        parsed_date = datetime.strptime(visit_date, '%Y-%m-%d').date()

        # Fetch paginated visits
        visits_paginated = visit_manager.get_all_visits_by_date_paginated_full(
            parsed_date, page=page, per_page=per_page, sort_order=sort_order
        )
    except ValueError as e:
        return jsonify({'message': f'Invalid input: {str(e)}'}), 400

    return jsonify(visits_paginated), 200


@bp.errorhandler(400)
@bp.errorhandler(401)
@bp.errorhandler(404)
@bp.errorhandler(500)
def handle_validation_error(error):
    return jsonify({
        'message': str(error.description)
    }), error.code


@bp.errorhandler(DataError)
def handle_integrity_error(error):
    return jsonify({
        'message': f'Database integrity error. {str(error.code)}'
    }), 409
