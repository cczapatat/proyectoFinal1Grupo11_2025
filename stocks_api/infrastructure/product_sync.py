import os
import requests
from sqlalchemy import asc
from ..config.db import db
from ..models.stock_model import ProductStock, Stock

# Constants
PRODUCTS_API_URL = os.getenv('PRODUCT_API', "http://127.0.0.1:3017")
ENDPOINT_LIST = "/products/list?all=true"
INTERNAL_TOKEN = os.getenv('INTERNAL_TOKEN', 'internal_token')


class ProductsSync:
    """Sync products from the product service to the stock table."""

    @staticmethod
    def sync_products() -> list[dict]:
        """Fetch products from the product service and sync them with the stock table."""
        products_json = ProductsSync._fetch_products_from_service()
        existing_product_ids = ProductsSync._get_existing_product_ids()
        products_to_add = ProductsSync._filter_new_products(products_json, existing_product_ids)

        if products_to_add:
            ProductsSync._add_new_products(products_json, products_to_add)

        return ProductsSync._get_added_products(products_to_add)

    @staticmethod
    def _fetch_products_from_service() -> list:
        """Fetch all products from the product service."""
        url = ProductsSync._ensure_url_has_protocol(f"{PRODUCTS_API_URL}{ENDPOINT_LIST}")
        headers = {'x-token': INTERNAL_TOKEN}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _get_existing_product_ids() -> set:
        """Get all distinct product IDs from the stock table."""
        return {product.id_product for product in db.session.query(ProductStock.id_product).distinct()}

    @staticmethod
    def _filter_new_products(products_json: list, existing_product_ids: set) -> list:
        """Find product IDs that are in the API but not in the database."""
        return [product['id'] for product in products_json if product['id'] not in existing_product_ids]

    @staticmethod
    def _add_new_products(products_json: list, products_to_add: list) -> None:
        """Add new products and initialize their stock."""
        products_map = {product['id']: product for product in products_json}

        new_products = [
            ProductStock(
                id_product=product['id'],
                product_name=product['name'],
                product_description=product['description'],
                product_category=product['category'],
                product_image=product['url_photo'],
            )
            for product_id in products_to_add if (product := products_map.get(product_id))
        ]

        new_stocks = [
            Stock(
                id_product=product_id,
                quantity_in_stock=0,
                last_quantity=0,
                enabled=True,
            )
            for product_id in products_to_add
        ]

        db.session.bulk_save_objects(new_products + new_stocks)
        db.session.commit()

    @staticmethod
    def _get_added_products(products_to_add: list) -> list[dict]:
        """Retrieve all the stocks added to the products table."""
        if not products_to_add:
            return []
        products_added = db.session.query(ProductStock).filter(ProductStock.id_product.in_(products_to_add)).all()
        return [product.to_dict() for product in products_added]

    @staticmethod
    def _ensure_url_has_protocol(url: str) -> str:
        """Ensure the URL has a protocol (http:// or https://)."""
        return url if url.startswith(('http://', 'https://')) else f"http://{url}"
