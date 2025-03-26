from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask import jsonify, make_response

from ..config.db import db
from ..models.product_model import Product
from ..dtos.product_dto import ProductDTO


class ProductRepository:

    @staticmethod
    def create_product(product_dto: ProductDTO) -> Product:
        product = Product()
        product.manufacturer_id = product_dto.manufacturer_id
        product.name = product_dto.name
        product.description = product_dto.description
        product.category = product_dto.category
        product.unit_price = product_dto.unit_price
        product.currency_price = product_dto.currency_price
        product.is_promotion = product_dto.is_promotion
        product.discount_price = product_dto.discount_price
        product.expired_at = product_dto.expired_at
        product.url_photo = product_dto.url_photo
        product.store_conditions = product_dto.store_conditions
        product.created_at = datetime.now()
        product.updated_at = datetime.now()

        try:
            db.session.add(product)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            response = make_response(
                jsonify({"error": "Integrity error", "message": str(e.orig)}), 400
            )
            return response
        except Exception as e:
            db.session.rollback()
            response = make_response(
                jsonify({"error": "Internal server error", "message": str(e)}), 500
            )
            return response

        return product