import os
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import Unauthorized

from ..dtos.seller_dto import SellerDTO
from ..infrastructure.seller_repository import SellerRepository
from ..models.seller_model import Seller

bp = Blueprint('sellers', __name__, url_prefix='/sellers')

internal_token = os.getenv('INTERNAL_TOKEN', default='internal_token')

seller_repository = SellerRepository()

def there_is_token():
    token = request.headers.get('x-token', None)

    if token is None:
        raise Unauthorized(description='authorization required')

    if token != internal_token:
        raise Unauthorized(description='authorization required')


@bp.route('/create', methods=('POST',))
def create_seller():
    there_is_token()
    
    data = request.get_json()
    user_id =  data.get('user_id')
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')
    zone = data.get('zone')
    quota_expected = data.get('quota_expected')
    currency_quota = data.get('currency_quota')
    quartely_target = data.get('quartely_target')
    currency_target = data.get('currency_target')
    performance_recomendations = data.get('performance_recomendations')

    if user_id is None:
        return jsonify({'message': 'user_id is required'}), 400
    
    if name is None:
        return jsonify({'message': 'name is required'}), 400
    
    if phone is None:
        return jsonify({'message': 'phone is required'}), 400
    
    if email is None:
        return jsonify({'message': 'email is required'}), 400
    
    if zone is None:
        return jsonify({'message': 'zone is required'}), 400
    
    if quota_expected is None:
        return jsonify({'message': 'quota_expected is required'}), 400
    
    if currency_quota is None:
        return jsonify({'message': 'currency_quota is required'}), 400
    
    if quartely_target is None:
        return jsonify({'message': 'quartely_target is required'}), 400
    
    if currency_target is None:
        return jsonify({'message': 'currency_target is required'}), 400
    
    if performance_recomendations is None:
        return jsonify({'message': 'performance_recomendations is required'}), 400
    

    seller_dto = SellerDTO(
        user_id=user_id,
        name=name,
        phone=phone,
        email=email,
        zone=zone,
        quota_expected=quota_expected,
        currency_quota=currency_quota,
        quartely_target=quartely_target,
        currency_target=currency_target,
        performance_recomendations=performance_recomendations
    )
    
    create_seller_response = seller_repository.create_seller(seller_dto=seller_dto)

    if isinstance(create_seller_response, Seller):
        return jsonify(create_seller_response.to_dict()), 201
    
    return create_seller_response

@bp.route('/<user_id>', methods=('GET',))
def get_seller_by_user_id(user_id: str):
    there_is_token()
    get_seller_response = seller_repository.get_seller_by_user_id(user_id=user_id)

    if get_seller_response is None:
        return jsonify({'message': 'seller not found'}), 404

    return jsonify(get_seller_response.to_dict()), 200