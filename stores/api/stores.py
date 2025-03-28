import os
import uuid
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import Unauthorized, BadRequest, NotFound
from flask_validate_json import validate_json
from sqlalchemy.exc import IntegrityError, DataError

from ..dtos.store_in_dto import StoreInDTO
from ..manager.store_manager import StoreManager
from ..models.enums import STATE, SECURITY_LEVEL
from ..schemas.store_schemas import STORE_SCHEMA

bp = Blueprint('stores', __name__, url_prefix='/stores')

internal_token = os.getenv('INTERNAL_TOKEN', default='internal_token')

store_manager = StoreManager()


def there_is_token():
    token = request.headers.get('x-token', None)

    if token is None:
        raise Unauthorized(description='authorization required')

    if token != internal_token:
        raise Unauthorized(description='authorization required')


@bp.route('/<id_store>', methods=('GET',))
def get_store_by_id(id_store: str):
    there_is_token()

    try:
        uuid.UUID(id_store)
    except ValueError:
        raise BadRequest(description='Invalid store id')

    store = store_manager.get_store_by_id(id_store)

    if store is None:
        raise NotFound(description='Store not found')

    return jsonify(store), 200


@bp.route('/', methods=('POST',))
@bp.route('/create', methods=('POST',))
@validate_json(STORE_SCHEMA)
def create_store():
    there_is_token()
    store_in_dto = _dict_to_store_in_dto(request.get_json())
    store = store_manager.create_store(store_in_dto)
    return jsonify(store), 201


def _dict_to_store_in_dto(data: dict) -> StoreInDTO:
    return StoreInDTO(
        name=data.get('name'),
        phone=data.get('phone'),
        email=data.get('email'),
        address=data.get('address'),
        capacity=data.get('capacity'),
        state=STATE[data.get('state')],
        security_level=SECURITY_LEVEL[data.get('security_level')],
    )


@bp.errorhandler(400)
@bp.errorhandler(401)
@bp.errorhandler(404)
def handle_validation_error(error):
    return jsonify({
        'message': str(error.description)
    }), error.code


@bp.errorhandler(IntegrityError)
@bp.errorhandler(DataError)
def handle_integrity_error(error):
    if 'unique_email' in str(error):
        return jsonify({
            'message': 'Email already exists'
        }), 400

    return jsonify({
        'message': f'Database integrity error. {str(error.code)}'
    }), 409
