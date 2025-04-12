import os
import uuid

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import Unauthorized, BadRequest

from ..config.db import db
from ..dtos.seller_dto import SellerDTO
from ..infrastructure.seller_repository import SellerRepository
from ..infrastructure.seller_sort_field import SellerSortField

from sqlalchemy.exc import IntegrityError, DataError

bp = Blueprint('sellers', __name__, url_prefix='/sellers')

internal_token = os.getenv('INTERNAL_TOKEN', default='internal_token')

seller_repository = SellerRepository(db.session)


def __there_is_token():
    token = request.headers.get('x-token', None)

    if token is None:
        raise Unauthorized(description='authorization required')

    if token != internal_token:
        raise Unauthorized(description='authorization required')


def __valid_uuid(uuid_string: str, uuid_name: str) -> uuid.uuid4:
    try:
        _uuid = uuid.UUID(uuid_string)

        return _uuid
    except ValueError:
        raise BadRequest(description=f'Invalid {uuid_name}')


@bp.route('/create', methods=('POST',))
def create_seller():
    __there_is_token()

    try:
        data = request.get_json()
        seller_dto = SellerDTO.from_dict(data)

        seller = seller_repository.create_seller(seller_dto.__dict__)
        print(seller.__dict__)
        db.session.commit()
        return jsonify(seller.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        print(e.__dict__)
        return jsonify({'message': str(e)}), 400


@bp.route('/<user_id>', methods=('GET',))
def get_seller_by_user_id(user_id: str):
    __there_is_token()
    _user_id = __valid_uuid(user_id, 'user_id')
    seller = seller_repository.get_seller_by_user_id(user_id=_user_id)

    if seller is None:
        return jsonify({'message': 'seller not found'}), 404

    return jsonify(seller.to_dict()), 200

@bp.route('/id/<id>', methods=('GET',))
def get_seller_by_id_full(id: str):
    __there_is_token()

    seller = seller_repository.get_seller_by_id_full(seller_id=id)

    if seller is None:
        return jsonify({'message': 'seller not found'}), 404

    return jsonify(seller.to_dict()), 200


@bp.route('/by-id/<seller_id>', methods=('GET',))
def get_seller_by_id(seller_id: str):
    __there_is_token()
    _user_id = __valid_uuid(seller_id, 'seller_id')
    seller = seller_repository.get_seller_by_id(seller_id=_user_id)

    if seller is None:
        return jsonify({'message': 'seller not found'}), 404

    return jsonify(seller.to_dict()), 200


@bp.route('/all', methods=('GET',))
def get_all_sellers():
    __there_is_token()
    sellers = seller_repository.get_all_sellers()

    return jsonify([seller.to_dict() for seller in sellers]), 200


@bp.errorhandler(400)
@bp.errorhandler(401)
@bp.errorhandler(404)
def handle_validation_error(error):
    return jsonify({
        'message': str(error.description)
    }), error.code


@bp.route('/sellers', methods=('GET',))
def get_sellers_paginated():
    __there_is_token()
    # Get query parameters with default values
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    sort_by_str = request.args.get('sort_by', default='name', type=str).lower()
    sort_order = request.args.get('sort_order', default='asc', type=str).lower()

    if sort_by_str not in [field.value for field in SellerSortField]:
        return jsonify({"message": f"Invalid sort_by field: {sort_by_str}"}), 400

    sort_by = SellerSortField(sort_by_str)
    """Get all sellers"""
    seller_data = seller_repository.get_sellers_paginated(
        page=page,
        per_page=per_page,
        sort_by=sort_by,
        sort_order=sort_order
    )

    return jsonify(seller_data), 200


@bp.errorhandler(IntegrityError)
@bp.errorhandler(DataError)
def handle_integrity_error(error):
    seller_repository.clean_transactions()
    if 'unique_client_email' in str(error):
        return jsonify({
            'message': 'Email already exists'
        }), 400
    if 'unique_client_phone' in str(error):
        return jsonify({
            'message': 'Phone already exists'
        }), 400
    if 'unique_client_user_id' in str(error):
        return jsonify({
            'message': 'Client already exists'
        }), 400
    if 'valid_client_email_format' in str(error):
        return jsonify({
            'message': 'Email format is not valid'
        }), 400
    if 'valid_client_phone_format' in str(error):
        return jsonify({
            'message': 'Phone format is not valid'
        }), 400
    return jsonify({
        'message': f'Database integrity error. {str(error.code)}'
    }), 409

