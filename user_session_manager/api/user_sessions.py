import os
import requests
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, current_user, jwt_required
from user_session_manager.models.data_classes import LoginIn
from werkzeug.exceptions import Unauthorized


from ..dtos.user_session_dto import UserSessionDTO
from ..infrastructure.user_session_repository import UserSessionRepository
from ..models.user_session_model import UserSession

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
        print(f"[Client] Failed to create client {url}, status code: {create_client_response.status_code}, response: {create_client_response.json()}")
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
    
    if  isinstance(create_user_session_response, UserSession):
        user_session = create_user_session_response.to_dict()

        if user_session['type'] == 'SELLER':
            seller = create_seller(request, user_session['id'])
        
            if seller is None:
                return jsonify({'message': 'failed to create seller'}), 500
        
            token_de_acceso = create_access_token(identity=LoginIn(
                user_session['id'],
                seller['id'],
                type
            ))

            seller['token'] = token_de_acceso

            return seller, 201
        
        if user_session['type'] == 'CLIENT':
            client = create_client(request, user_session['id'])
        
            if client is None:
                return jsonify({'message': 'failed to create client'}), 500
        
            token_de_acceso = create_access_token(identity=LoginIn(
                user_session['id'],
                client['id'],
                type
            ))

            client['token'] = token_de_acceso

            return client, 201 

    
    return create_user_session_response


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
        access_token = create_access_token(identity=LoginIn(
            user_session['id'],
            None,
            user_session['type']
        ))

        user_session['token'] = access_token

        return user_session, 200

    if user_session['type'] == 'SELLER':
        seller = get_seller_by_user_id(request, user_session['id'])
        
        if seller is None:
            return jsonify({'message': 'invalid credentials'}), 401
        
        access_token = create_access_token(identity=LoginIn(
            user_session['id'],
            seller['id'],
            user_session['type']
        ))

        seller['type'] = user_session['type']
        seller['token'] = access_token

        return seller, 200
    
    if user_session['type'] == 'CLIENT':
        client = get_client_by_user_id(request, user_session['id'])
        
        if client is None:
            return jsonify({'message': 'invalid credentials'}), 401
        
        access_token = create_access_token(identity=LoginIn(
            user_session['id'],
            client['id'],
            user_session['type']
        ))
        client['type'] = user_session['type']
        client['token'] = access_token

        return client, 200
    

