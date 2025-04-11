import uuid
from datetime import datetime

from flask import jsonify, make_response
from sqlalchemy.exc import IntegrityError

from .cache_repository import CacheRepository
from ..config.db import db
from ..dtos.product_dto import ProductDTO
from ..models.product_model import Product

cache_repository = CacheRepository()


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

    @staticmethod
    def get_product_by_id(product_id: str) -> Product:
        product = Product.query.get(product_id)
        if not product:
            response = make_response(
                jsonify({"error": "Product not found", "message": "Product not found"}), 404
            )
            return response

        return product

    @staticmethod
    def update_product(product_id: str, product_dto: ProductDTO) -> Product:
        product = Product.query.get(product_id)
        if not product:
            response = make_response(
                jsonify({"error": "Product not found", "message": "Product not found"}), 404
            )

            return response

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
        product.updated_at = datetime.now()

        try:
            db.session.commit()
            cache_repository.delete(f"product:{product_id}")
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

    @staticmethod
    def get_all_products() -> list[Product]:
        products = Product.query.all()

        return products
    
    @staticmethod
    def get_products_by_page(page: int, per_page: int) -> list[Product]:
        offset = (page - 1) * per_page
        products = Product.query.offset(offset).limit(per_page).all()

        return products

    @staticmethod
    def get_products_by_ids(ids: list[uuid.uuid4]) -> list[Product]:
        cache_keys = [f"product:{product_id}" for product_id in ids]
        products_cached = cache_repository.get_multiple(cache_keys)
        ids_cached = [cached['id'] for cached in products_cached]
        if products_cached:
            ids = [product_id for product_id in ids if product_id not in ids_cached]

        if len(ids) == 0:
            return products_cached
        else:
            products = Product.query.filter(Product.id.in_(ids)).all()

        for product in products:
            cache_repository.set(f"product:{product.id}", product.to_dict())

        return [product.to_dict() for product in products] + products_cached
