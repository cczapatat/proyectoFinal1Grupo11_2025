import os
import uuid

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError, DataError

from werkzeug.exceptions import Unauthorized, BadRequest

from ..dtos.client_dto import ClientDTO
from ..infrastructure.client_repository import ClientRepository, get_clients_by_seller_id, \
    get_clients_by_seller_id_paginated
from ..infrastructure.client_sort_field import ClientSortField
from ..models.client_model import Client

bp = Blueprint('clients', __name__, url_prefix='/clients')

internal_token = os.getenv('INTERNAL_TOKEN', default='internal_token')

client_repository = ClientRepository()


def there_is_token():
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
def create_client():
    there_is_token()

    data = request.get_json()
    user_id = data.get('user_id')
    seller_id = data.get('seller_id')
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')
    address = data.get('address')
    client_type = data.get('client_type')
    zone = data.get('zone')

    if user_id is None:
        return jsonify({'message': 'user_id is required'}), 400

    if name is None:
        return jsonify({'message': 'name is required'}), 400

    if phone is None:
        return jsonify({'message': 'phone is required'}), 400

    if email is None:
        return jsonify({'message': 'email is required'}), 400

    if address is None:
        return jsonify({'message': 'address is required'}), 400

    if client_type is None:
        return jsonify({'message': 'type is required'}), 400

    if zone is None:
        return jsonify({'message': 'zone is required'}), 400

    client_dto = ClientDTO(
        user_id=user_id,
        seller_id=seller_id,
        name=name,
        phone=phone,
        email=email,
        address=address,
        client_type=client_type,
        zone=zone
    )

    create_client_response, saved_seller_id = client_repository.create_client(client_dto=client_dto)

    if isinstance(create_client_response, Client):
        response_client = create_client_response.to_dict()
        response_client.setdefault("seller_id", saved_seller_id)
        return jsonify(response_client), 201

    return create_client_response


@bp.route('/<user_id>', methods=('GET',))
def get_client_by_user_id(user_id: str):
    there_is_token()
    get_client_response = client_repository.get_client_by_user_id(user_id=user_id)

    if get_client_response is None:
        return jsonify({'message': 'client not found'}), 404

    return jsonify(get_client_response.to_dict()), 200


@bp.route('/seller-info/<user_id>', methods=('GET',))
def get_client_by_user_id_with_seller(user_id: str):
    there_is_token()
    get_client_response = client_repository.get_client_by_user_id_with_seller(user_id=user_id)
    if get_client_response is None:
        return jsonify({'message': 'client not found'}), 404

    return jsonify(get_client_response), 200


@bp.route('/seller/<string:seller_id>', methods=['GET'])
def get_seller_clients(seller_id):
    there_is_token()
    """Get all clients for a specific seller"""
    clients = get_clients_by_seller_id(seller_id)

    if clients is None:
        return jsonify({'message': 'clients not found'}), 404

    return jsonify(clients), 200


@bp.route('/client-id/<client_id>/seller-id/<seller_id>', methods=('GET',))
def get_seller_by_id(client_id: str, seller_id: str):
    there_is_token()
    _client_id = __valid_uuid(client_id, 'client_id')
    _seller_id = __valid_uuid(seller_id, 'seller_id')
    client = client_repository.get_client_relation_seller(
        client_id=_client_id,
        seller_id=_seller_id,
    )

    if client is None:
        return jsonify({'message': 'client not found'}), 404

    return jsonify(client.to_dict()), 200


@bp.route('/associate_seller', methods=('POST',))
def associate_seller():
    there_is_token()

    data = request.get_json()
    client_id = data.get('client_id')
    seller_id = data.get('seller_id')

    if client_id is None:
        return jsonify({'message': 'client_id is required'}), 400

    if seller_id is None:
        return jsonify({'message': 'seller_id is required'}), 400

    client, missing_clients = client_repository.get_clients_by_ids(client_ids=client_id)

    if missing_clients > 0:
        return jsonify({'message': 'clients not found'}), 404

    # Get query parameters with default values
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    sort_by_str = request.args.get('sort_by', default='name', type=str).lower()
    sort_order = request.args.get('sort_order', default='asc', type=str).lower()

    if sort_by_str not in [field.value for field in ClientSortField]:
        return jsonify({"message": f"Invalid sort_by field: {sort_by_str}"}), 400

    sort_by = ClientSortField(sort_by_str)

    clients = client_repository.associate_seller(client_id, seller_id, page=page,
        per_page=per_page,
        sort_by=sort_by,
        sort_order=sort_order)

    if clients is None:
        return jsonify({'message': 'clients not found'}), 404

    return jsonify(clients), 200


@bp.route('/seller/pag/<string:seller_id>', methods=['GET'])
def get_seller_clients_paginated(seller_id):
    there_is_token()
    # Get query parameters with default values
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    sort_by_str = request.args.get('sort_by', default='name', type=str).lower()
    sort_order = request.args.get('sort_order', default='asc', type=str).lower()

    if sort_by_str not in [field.value for field in ClientSortField]:
        return jsonify({"message": f"Invalid sort_by field: {sort_by_str}"}), 400


    sort_by = ClientSortField(sort_by_str)
    """Get all clients for a specific seller"""
    clients_data = get_clients_by_seller_id_paginated(
        seller_id=seller_id,
        page=page,
        per_page=per_page,
        sort_by=sort_by,
        sort_order=sort_order
    )

    return jsonify(clients_data), 200

@bp.route('/clients/pag', methods=('GET',))
def get_all_clients_paginated():
    there_is_token()
    # Get query parameters with default values
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    sort_by_str = request.args.get('sort_by', default='name', type=str).lower()
    sort_order = request.args.get('sort_order', default='asc', type=str).lower()

    if sort_by_str not in [field.value for field in ClientSortField]:
        return jsonify({"message": f"Invalid sort_by field: {sort_by_str}"}), 400

    sort_by = ClientSortField(sort_by_str)
    """Get all sellers"""
    seller_data = client_repository.get_clients_paginated(
        page=page,
        per_page=per_page,
        sort_by=sort_by,
        sort_order=sort_order
    )

    return jsonify(seller_data), 200


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
    client_repository.clean_transactions()
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
