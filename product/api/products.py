import os

from datetime import datetime
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import Unauthorized

from ..dtos.product_dto import ProductDTO
from ..infrastructure.product_repository import ProductRepository
from ..models.product_model import CATEGORY_PRODUCT, CURRENCY_PRODUCT, Product


bp = Blueprint('products', __name__, url_prefix='/products')

internal_token = os.getenv('INTERNAL_TOKEN', default='internal_token')

product_repository = ProductRepository()

def there_is_token():
    token = request.headers.get('x-token', None)

    if token is None:
        raise Unauthorized(description='authorization required')

    if token != internal_token:
        raise Unauthorized(description='authorization required')


@bp.route('/create', methods=('POST',))
def create_product():
    there_is_token()
    
    data = request.get_json()
    manufacturer_id =  data.get('manufacturer_id')
    name = data.get('name')
    description = data.get('description')
    category = data.get('category')
    unit_price = data.get('unit_price')
    currency_price = data.get('currency_price')
    is_promotion = data.get('is_promotion')
    discount_price = data.get('discount_price')
    expired_at = data.get('expired_at')
    url_photo = data.get('url_photo')
    store_conditions = data.get('store_conditions')


    if manufacturer_id is None:
        return jsonify({'message': 'manufacturer_id is required'}), 400
    
    if name is None:
        return jsonify({'message': 'name is required'}), 400
    
    if description is None:
        return jsonify({'message': 'description is required'}), 400
    
    if category is None:
        return jsonify({'message': 'category is required'}), 400
    
    if unit_price is None:
        return jsonify({'message': 'unit_price is required'}), 400
    
    if currency_price is None:
        return jsonify({'message': 'currency_price is required'}), 400
    
    if is_promotion is None:
        return jsonify({'message': 'is_promotion is required'}), 400
    
    if discount_price is None:
        return jsonify({'message': 'discount_price is required'}), 400
    
    try:
        if expired_at is not None and datetime.fromisoformat(expired_at) <= datetime.now():
            return jsonify({'message': 'expired_at must be a future date'}), 400
    except ValueError:
        return jsonify({'message': 'expired_at must be a valid date'}), 400
    
    if url_photo is None:
        return jsonify({'message': 'url_photo is required'}), 400
    
    if store_conditions is None:
        return jsonify({'message': 'store_conditions is required'}), 400
    

    product_dto = ProductDTO(
        manufacturer_id=manufacturer_id,
        name=name,
        description=description,
        category=category,
        unit_price=unit_price,
        currency_price=currency_price,
        is_promotion=is_promotion,
        discount_price=discount_price,
        expired_at=expired_at,
        url_photo=url_photo,
        store_conditions=store_conditions
    )
    
    create_product_response = product_repository.create_product(product_dto=product_dto)

    if isinstance(create_product_response, Product):
        return jsonify(create_product_response.to_dict()), 201
    
    return create_product_response

@bp.route('/get/<product_id>', methods=('GET',))
def get_product(product_id):
    there_is_token()
    
    product = product_repository.get_product_by_id(product_id)

    if isinstance(product, Product):
        return jsonify(product.to_dict()), 200
    
    return product

@bp.route('/update/<product_id>', methods=('PUT',))
def update_product(product_id):
    there_is_token()
    
    data = request.get_json()
    manufacturer_id = data.get('manufacturer_id')
    name = data.get('name')
    description = data.get('description')
    category = data.get('category')
    unit_price = data.get('unit_price')
    currency_price = data.get('currency_price')
    is_promotion = data.get('is_promotion')
    discount_price = data.get('discount_price')
    expired_at = data.get('expired_at')
    url_photo = data.get('url_photo')
    store_conditions = data.get('store_conditions')

    if manufacturer_id is None:
        return jsonify({'message': 'manufacturer_id is required'}), 400
    
    if name is None:
        return jsonify({'message': 'name is required'}), 400
    
    if description is None:
        return jsonify({'message': 'description is required'}), 400
    
    if category is None:
        return jsonify({'message': 'category is required'}), 400
    
    if unit_price is None:
        return jsonify({'message': 'unit_price is required'}), 400
    
    if currency_price is None:
        return jsonify({'message': 'currency_price is required'}), 400
    
    if is_promotion is None:
        return jsonify({'message': 'is_promotion is required'}), 400
    
    if discount_price is None:
        return jsonify({'message': 'discount_price is required'}), 400
    
    try:
        if expired_at is not None and datetime.fromisoformat(expired_at) <= datetime.now():
            return jsonify({'message': 'expired_at must be a future date'}), 400
    except ValueError:
        return jsonify({'message': 'expired_at must be a valid date'}), 400
    
    if url_photo is None:
        return jsonify({'message': 'url_photo is required'}), 400
    
    if store_conditions is None:
        return jsonify({'message': 'store_conditions is required'}), 400

    product_dto = ProductDTO(
        manufacturer_id=manufacturer_id,
        name=name,
        description=description,
        category=category,
        unit_price=unit_price,
        currency_price=currency_price,
        is_promotion=is_promotion,
        discount_price=discount_price,
        expired_at=expired_at,
        url_photo=url_photo,
        store_conditions=store_conditions
    )

    update_product_response = product_repository.update_product(product_id, product_dto)

    if isinstance(update_product_response, Product):
        return jsonify(update_product_response.to_dict()), 200
    
    return update_product_response

@bp.route('/categories', methods=('GET',))
def get_all_categories():
    there_is_token()
    
    categories = [{"key": category.name, "value": category.value} for category in CATEGORY_PRODUCT]


    return jsonify(categories), 200

@bp.route('/currencies', methods=('GET',))
def get_all_currencies():
    there_is_token

    currencies = [
        {"key": currency.name, "value": currency.value} for currency in CURRENCY_PRODUCT
    ]
    return jsonify(currencies), 200