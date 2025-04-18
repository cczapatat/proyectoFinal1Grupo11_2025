import os
import uuid
from datetime import datetime
from threading import Thread
from flask import current_app, Blueprint, jsonify, request
from werkzeug.exceptions import Unauthorized, BadRequest

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


def __valid_uuid(uuid_string: str) -> uuid.uuid4:
    try:
        uuid.UUID(uuid_string)
    except ValueError:
        raise BadRequest(description='invalids product ids')


@bp.route('/create', methods=('POST',))
def create_product():
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

@bp.route('/massive/update', methods=('PUT',))
def update_massive_products():
    there_is_token()
    
    # Parse the JSON data from the request
    data = request.get_json()

    # Validate that the data is a list and contains products
    if not isinstance(data, list) or len(data) == 0:
        return jsonify({'message': 'products is required and must be a non-empty array'}), 400

    products_to_update = []

    # Iterate over the products in the data array
    for index, product in enumerate(data):
        id = product.get('id')
        manufacturer_id = product.get('manufacturer_id')
        name = product.get('name')
        description = product.get('description')
        category = product.get('category')
        unit_price = product.get('unit_price')
        currency_price = product.get('currency_price')
        is_promotion = product.get('is_promotion')
        discount_price = product.get('discount_price')
        expired_at = product.get('expired_at')
        url_photo = product.get('url_photo')
        store_conditions = product.get('store_conditions')

        # Validate required fields for each product
        if id is None:
            return jsonify({'message': f'products[{index}].id is required'}), 400
        if manufacturer_id is None:
            return jsonify({'message': f'products[{index}].manufacturer_id is required'}), 400
        if name is None:
            return jsonify({'message': f'products[{index}].name is required'}), 400
        if description is None:
            return jsonify({'message': f'products[{index}].description is required'}), 400
        if category is None:
            return jsonify({'message': f'products[{index}].category is required'}), 400
        if unit_price is None:
            return jsonify({'message': f'products[{index}].unit_price is required'}), 400
        if currency_price is None:
            return jsonify({'message': f'products[{index}].currency_price is required'}), 400
        if is_promotion is None:
            return jsonify({'message': f'products[{index}].is_promotion is required'}), 400
        if discount_price is None:
            return jsonify({'message': f'products[{index}].discount_price is required'}), 400
        try:
            if expired_at is not None and datetime.fromisoformat(expired_at) <= datetime.now():
                return jsonify({'message': f'products[{index}].expired_at must be a future date'}), 400
        except ValueError:
            return jsonify({'message': f'products[{index}].expired_at must be a valid date'}), 400
        if url_photo is None:
            return jsonify({'message': f'products[{index}].url_photo is required'}), 400
        if store_conditions is None:
            return jsonify({'message': f'products[{index}].store_conditions is required'}), 400

        # Create a Product object for each valid product
        product_to_update = Product(
            id=id,
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
        products_to_update.append(product_to_update)

    # Run the update operation in a separate thread
    def update_products_async(app, products):
        with app.app_context():  # Push the application context
            product_repository.update_massive_products(products)

    # Pass the current Flask app to the thread
    app = current_app._get_current_object()
    Thread(target=update_products_async, args=(app, products_to_update)).start()

    # Immediately return a response
    return jsonify({'message': 'The update operation is being processed in the background'}), 202

@bp.route('/list', methods=('GET',))
def list_products():
    there_is_token()

    page = max(1, request.args.get('page', default=1, type=int))
    per_page = min(max(1, request.args.get('per_page', default=10, type=int)), 50)
    all_products = request.args.get('all', default=False, type=bool)

    if all_products:
        products = product_repository.get_all_products()
        return jsonify([product.to_dict() for product in products]), 200

    products = product_repository.get_products_by_page(page=page, per_page=per_page)

    if isinstance(products, list):
        return jsonify([product.to_dict() for product in products]), 200

    return products


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

@bp.route('/paginated_full', methods=['GET'])
def get_products_paginated_full():
    there_is_token()  

    
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    # Por ahora el único campo de ordenación es 'name'
    sort_order = request.args.get('sort_order', default='asc', type=str).lower()
   
    products_data = product_repository.get_products_paginated_full(page=page, per_page=per_page, sort_order=sort_order)

    return jsonify(products_data), 200


@bp.route('/by-ids', methods=('POST',))
def get_products_by_ids():
    there_is_token()

    ids = request.get_json().get('ids', None)

    if ids is None:
        return jsonify({'message': 'ids is required'}), 400

    if not isinstance(ids, list):
        return jsonify({'message': 'ids must be a list'}), 400

    if len(ids) == 0:
        return jsonify({'message': 'ids cannot be empty'}), 400

    for id in ids:
        __valid_uuid(id)

    products_dict = product_repository.get_products_by_ids(ids)

    return jsonify(products_dict), 200


@bp.errorhandler(400)
@bp.errorhandler(401)
@bp.errorhandler(404)
def handle_validation_error(error):
    return jsonify({
        'message': str(error.description)
    }), error.code
