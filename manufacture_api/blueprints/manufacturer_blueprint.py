import os

import requests
from flask import request, Blueprint, jsonify
from werkzeug.exceptions import Unauthorized, InternalServerError

from ..commands.create_manufacturer import CreateManufacturer
from ..commands.create_massive_manufacturer import CreateMassiveManufacturer
from ..commands.get_all_manufacturer import GetAllManufacturer
from ..commands.get_paginate_manufacturer import GetPaginateManufacturer
from ..commands.get_total_manufacturers import GetTotalManufacturers
from ..models.Models import BulkTaskSchema
from ..validators.validators import validate_token

manufacturer_blueprint = Blueprint('manufacturers', __name__, url_prefix='/manufacture-api')
bulk_task_schema = BulkTaskSchema()
internal_token = os.getenv('INTERNAL_TOKEN', default='internal_token')
user_session_manager_path = os.getenv('USER_SESSION_MANAGER_PATH', default='http://localhost:3008')


def there_is_token():
    token = request.headers.get('x-token', None)

    if token is None:
        raise Unauthorized(description='authorization required')

    if token != internal_token:
        raise Unauthorized(description='authorization required')


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


def get_json_data(keys):
    return {key: request.get_json()[key] for key in keys}


@manufacturer_blueprint.route('/manufacturers/create', methods=['POST'])
def create():
    validate_token(request.headers)

    data = get_json_data([
        'name',
        'address',
        'phone',
        'email',
        'country',
        'tax_conditions',
        'legal_conditions',
        'rating_quality',
    ])

    print(data)

    manufacturer = CreateManufacturer(**data)
    manufacturer_response = manufacturer.execute()
    return jsonify(manufacturer_response), 201


@manufacturer_blueprint.route('/manufacturers/all', methods=['GET'])
def get_all_manufacturer():
    validate_token(request.headers)
    get_all_manufacturers = GetAllManufacturer()
    get_all_manufacturers_response = get_all_manufacturers.execute()
    return jsonify(get_all_manufacturers_response), 200


@manufacturer_blueprint.route('/manufacturers/list', methods=['GET'])
def get_paginate_manufacturer():
    validate_token(request.headers)
    page = max(1, request.args.get('page', default=1, type=int))
    per_page = min(max(1, request.args.get('per_page', default=10, type=int)), 50)

    _get_total_manufacturers = GetTotalManufacturers()
    get_total_manufacturers_response = _get_total_manufacturers.execute()
    _get_paginate_manufacturer = GetPaginateManufacturer(page, per_page)
    get_paginate_manufacturer_response = _get_paginate_manufacturer.execute()
    return jsonify({
        'total': get_total_manufacturers_response,
        'manufacturers': get_paginate_manufacturer_response,
        'page': page,
        'per_page': per_page
    }), 200


@manufacturer_blueprint.route('/manufacturers/massive/create', methods=('POST',))
def create_massive_manufacturers():
    there_is_token()
    user_auth = __validate_auth_token()

    if user_auth['user_type'] == 'ADMIN':
        user_id = user_auth['user_session_id']
    elif user_auth['user_type'] == 'SELLER':
        user_id = user_auth['user_id']
    else:
        return jsonify({'message': 'Invalid user type'}), 403

    data = request.get_json()
    file_id = data.get('file_id')

    if file_id is None:
        return jsonify({'message': 'file_id is required'}), 400

    create_massive_manufacturer = CreateMassiveManufacturer(user_id, file_id)
    return create_massive_manufacturer.execute()
