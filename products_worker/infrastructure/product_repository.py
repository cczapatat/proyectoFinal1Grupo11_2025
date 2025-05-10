import uuid

from ..dtos.product_dto import ProductDTO
from ..models.product_model import Product
from ..models.declarative_base import session


class ProductRepository:
    @staticmethod
    def create_massive_products(transaction_id:str, productsDto: list[ProductDTO]) -> list[Product]:
        products = []

        for productDto in productsDto:
            product = Product()
            product.manufacturer_id = uuid.UUID(productDto.manufacturer_id)
            product.name = productDto.name
            product.description = productDto.description
            product.category = productDto.category
            product.unit_price = productDto.unit_price
            product.currency_price = productDto.currency_price
            product.is_promotion = bool(productDto.is_promotion)
            product.discount_price = productDto.discount_price
            product.expired_at = productDto.expired_at
            product.url_photo = productDto.url_photo
            product.store_conditions = productDto.store_conditions
            
            products.append(product)
        
        try:
            session.bulk_save_objects(products)
            session.commit()
            return products
        except Exception as ex:
            session.rollback()
            print(f"[Create Massive Products] process_id: {transaction_id}, error: {ex}")
            return []
        
    @staticmethod
    def update_massive_products(transaction_id:str, products: dict) -> list[Product]:
        try:
            session.bulk_update_mappings(Product, products)
            session.commit()
            return products
        except Exception as ex:
            session.rollback()
            print(f"[Update Massive Products] process_id: {transaction_id}, error: {ex}")
            return []
    
    @staticmethod
    def get_existing_product_ids(product_ids):
        try:
            existing_product_ids = session.query(Product.id).filter(Product.id.in_(product_ids)).all()
            return [str(product_id[0]) for product_id in existing_product_ids]
        except Exception as ex:
            print(f"[Get Existing Product IDs] error: {ex}")
            return []