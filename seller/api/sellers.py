import os
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import Unauthorized

from ..dtos.seller_dto import SellerDTO
from ..infrastructure.seller_repository import SellerRepository
from ..models.seller_model import Seller
from ..config.db import db

bp = Blueprint('sellers', __name__, url_prefix='/sellers')

internal_token = os.getenv('INTERNAL_TOKEN', default='internal_token')

def get_repository():
    return SellerRepository(db.session)

def there_is_token():
    token = request.headers.get('x-token', None)

    if token is None:
        raise Unauthorized(description='authorization required')

    if token != internal_token:
        raise Unauthorized(description='authorization required')

@bp.route('/create', methods=('POST',))
def create_seller():
    there_is_token()
    
    try:
        data = request.get_json()
        seller_dto = SellerDTO.from_dict(data)
    
        seller_repository = get_repository()

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
    there_is_token()
    try:
        seller_repository = get_repository()
        seller = seller_repository.get_seller_by_user_id(user_id=user_id)

        if seller is None:
            return jsonify({'message': 'seller not found'}), 404

        return jsonify(seller.to_dict()), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
