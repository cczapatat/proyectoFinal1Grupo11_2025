import json
import os
import requests
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, current_user, jwt_required
from werkzeug.exceptions import Unauthorized

from .client_sort_field import ClientSortField
from .seller_sort_field import SellerSortField
from ..dtos.user_session_dto import UserSessionDTO
from ..infrastructure.user_session_repository import UserSessionRepository
from ..models.user_session_model import UserSession
from ..models.data_classes import LoginIn

bp = Blueprint('user_sessions', __name__, url_prefix='/user_sessions')
host_seller = os.environ.get('SELLERS_PATH', 'http://localhost:3007')
host_client = os.environ.get('CLIENTS_PATH', 'http://localhost:3009')

internal_token = os.getenv('INTERNAL_TOKEN', default='internal_token')

user_session_repository = UserSessionRepository()


def there_is_token():
    token = request.headers.get('x-token', None)

    if token is None:
        raise Unauthorized(description='authorization required')

    if token != internal_token:
        raise Unauthorized(description='authorization required')


def create_seller(request, user_id):
    url = f"{host_seller}/sellers/create"
    data = request.get_json()
    data['user_id'] = user_id
    headers = request.headers
    create_seller_response = requests.post(url, json=data, headers=headers)

    if create_seller_response.status_code != 201:
        print(f"[Seller] Failed to create seller {url}, status code: {create_seller_response.status_code}")
        return None

    return create_seller_response.json()


def create_client(request, user_id):
    url = f"{host_client}/clients/create"
    data = request.get_json()
    data['user_id'] = user_id
    headers = request.headers
    create_client_response = requests.post(url, json=data, headers=headers)

    if create_client_response.status_code != 201:
        print(
            f"[Client] Failed to create client {url}, status code: {create_client_response.status_code}, response: {create_client_response.json()}")
        return None

    return create_client_response.json()


def get_seller_by_user_id(request, user_id):
    url = f"{host_seller}/sellers/{user_id}"
    headers = request.headers
    get_seller_response = requests.get(url, headers=headers)

    if get_seller_response.status_code != 200:
        print(f"[Seller] Failed to get seller {url}, status code: {get_seller_response.status_code}")
        return None

    return get_seller_response.json()


def get_client_by_user_id(request, user_id):
    url = f"{host_client}/clients/{user_id}"
    headers = request.headers
    get_client_response = requests.get(url, headers=headers)

    if get_client_response.status_code != 200:
        print(f"[Client] Failed to get client {url}, status code: {get_client_response.status_code}")
        return None

    return get_client_response.json()


@bp.route('/create', methods=('POST',))
def create_user_session():
    there_is_token()

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    type = data.get('type')

    if email is None:
        return jsonify({'message': 'email is required'}), 400

    if password is None:
        return jsonify({'message': 'password is required'}), 400

    if type is None:
        return jsonify({'message': 'type is required'}), 400

    if type not in ['SELLER', 'CLIENT', 'ADMIN']:
        return jsonify({'message': 'invalid type'}), 400

    user_session_dto = UserSessionDTO(
        email=email,
        password=password,
        type=type
    )

    create_user_session_response = user_session_repository.create_user_session(user_session_dto=user_session_dto)
    user_session = create_user_session_response.to_dict()

    if isinstance(create_user_session_response, UserSession):

        if user_session['type'] == 'SELLER':
            seller = create_seller(request, user_session['id'])

            if seller is None:
                return jsonify({'message': 'failed to create seller'}), 500

            token_access = create_access_token(
                identity=LoginIn(user_session['id'], seller['id'], type).to_serializable())
            seller['token'] = token_access

            return seller, 201

        if user_session['type'] == 'CLIENT':
            client = create_client(request, user_session['id'])

            if client is None:
                return jsonify({'message': 'failed to create client'}), 500

            token_access = create_access_token(
                identity=LoginIn(user_session['id'], client['id'], type).to_serializable())

            client['token'] = token_access

            return client, 201

    return user_session


@bp.route('/login', methods=('POST',))
def log_in():
    there_is_token()
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    get_user_session_by_credentials_response = user_session_repository.get_user_session_by_credentials(email, password)

    if get_user_session_by_credentials_response is None:
        return jsonify({'message': 'invalid credentials'}), 401

    user_session = get_user_session_by_credentials_response.to_dict()

    if user_session['type'] == 'ADMIN':
        access_token = create_access_token(
            identity=LoginIn(user_session['id'], 0, user_session['type']).to_serializable())

        user_session['token'] = access_token

        return user_session, 200

    if user_session['type'] == 'SELLER':
        seller = get_seller_by_user_id(request, user_session['id'])

        if seller is None:
            return jsonify({'message': 'invalid credentials'}), 401

        access_token = create_access_token(
            identity=LoginIn(user_session['id'], seller['id'], user_session['type']).to_serializable())

        seller['type'] = user_session['type']
        seller['token'] = access_token

        return seller, 200

    if user_session['type'] == 'CLIENT':
        client = get_client_by_user_id(request, user_session['id'])

        if client is None:
            return jsonify({'message': 'invalid credentials'}), 401

        access_token = create_access_token(
            identity=LoginIn(user_session['id'], client['id'], user_session['type']).to_serializable())
        client['type'] = user_session['type']
        client['token'] = access_token

        return client, 200


@bp.route('/auth', methods=['GET'])
@jwt_required()
def validate_token():
    identity = current_user
    if not identity:
        return jsonify({"error": "Invalid token"}), 401

    identity: LoginIn

    return jsonify({
        "user_session_id": identity.id,
        "user_id": identity.id_user,
        "user_type": identity.type
    }), 200


@bp.route('/clients/seller/<seller_id>', methods=('GET',))
def get_clients_by_seller(seller_id:str):
    there_is_token()

    # Get query parameters with default values
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    sort_by_str = request.args.get('sort_by', default='name', type=str).lower()
    sort_order = request.args.get('sort_order', default='asc', type=str).lower()

    if sort_by_str not in [field.value for field in ClientSortField]:
        return jsonify({"message": f"Invalid sort_by field: {sort_by_str}"}), 400

    sort_by = ClientSortField(sort_by_str).value
    """Get all clients for a specific seller"""

    url = f"{host_client}/clients/seller/{seller_id}?page={page}&per_page={per_page}&sort_by={sort_by}&sort_order={sort_order}"
    headers = request.headers
    get_client_response = requests.get(url, headers=headers)
    data = get_client_response.json()
    if get_client_response.status_code != 200:
        print(f"[Client] Failed to get clients {url}, status code: {get_client_response.status_code}")
        return jsonify(data),  get_client_response.status_code

    return get_client_response.json()


@bp.route('/clients/associate_seller', methods=('POST',))
def associate_client_to_seller():
    there_is_token()

    data = request.get_json()

    url = f"{host_client}/clients/associate_seller"
    headers = request.headers
    associate_client_response = requests.post(url, json=data, headers=headers)
    data = associate_client_response.json()
    if associate_client_response.status_code != 200:
        print(f"[Client] Failed to associate clients {url}, status code: {associate_client_response.status_code}")
        return jsonify(data),  associate_client_response.status_code

    return jsonify(associate_client_response.json()), 200

@bp.route('/sellers', methods=('GET',))
def get_sellers():
    there_is_token()

    # Get query parameters with default values
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    sort_by_str = request.args.get('sort_by', default='name', type=str).lower()
    sort_order = request.args.get('sort_order', default='asc', type=str).lower()

    if sort_by_str not in [field.value for field in ClientSortField]:
        return jsonify({"message": f"Invalid sort_by field: {sort_by_str}"}), 400

    sort_by = SellerSortField(sort_by_str).value
    """Get all sellers"""

    url = f"{host_seller}/sellers?page={page}&per_page={per_page}&sort_by={sort_by}&sort_order={sort_order}"
    headers = request.headers
    get_sellers_response = requests.get(url, headers=headers)
    data = get_sellers_response.json()
    if get_sellers_response.status_code != 200:
        return jsonify(data),  get_sellers_response.status_code

    return get_sellers_response.json()

@bp.route('/sellers/id/<id>', methods=('GET',))
def get_seller_by_id(id: str):
    url = f"{host_seller}/sellers/id/{id}"
    headers = request.headers
    get_seller_response = requests.get(url, headers=headers)
    data = get_seller_response.json()
    if get_seller_response.status_code != 200:
        return jsonify(data),  get_seller_response.status_code

    return get_seller_response.json()