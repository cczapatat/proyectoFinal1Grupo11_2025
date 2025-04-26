from faker import Faker
from products_worker.dtos.product_dto import ProductDTO
from products_worker.infrastructure.product_repository import ProductRepository
from products_worker.models.product_model import CATEGORY_PRODUCT, CURRENCY_PRODUCT, Product
from products_worker.models.declarative_base import session
import products_worker.init_bd

class TestProductRepository:
    def setup_method(self):
        self.data_factory = Faker()
        session.rollback()
        session.query(Product).delete()
        session.commit()
        self.process_id = str(self.data_factory.uuid4())
        


    def test_create_massive_products_success(self):
        products = []
        for _ in range(5):
            product = ProductDTO(
                manufacturer_id=str(self.data_factory.uuid4()),
                name=self.data_factory.name(),
                description=self.data_factory.word(),
                category=self.data_factory.random_element(
                    [category.value for category in CATEGORY_PRODUCT]),
                unit_price=self.data_factory.random_number(digits=2),
                currency_price=self.data_factory.random_element(
                    [currency.value for currency in CURRENCY_PRODUCT]),
                is_promotion=self.data_factory.boolean(),
                discount_price=self.data_factory.random_number(digits=2),
                expired_at=self.data_factory.date_time(),
                url_photo=self.data_factory.image_url(),
                store_conditions=self.data_factory.text()
            )
            products.append(product)
        
        result = ProductRepository.create_massive_products(self.process_id, products)
        
        assert len(result) == len(products)
    
    def test_create_massive_products_empty_list(self):
        products = []
        result = ProductRepository.create_massive_products(self.process_id, products)
        
        assert len(result) == 0

    def test_create_massive_products_integrity_error(self):
        product = ProductDTO(
            manufacturer_id=str(self.data_factory.uuid4()),
            name=self.data_factory.name(),
            description=self.data_factory.word(),
            category= "bad_category",
            unit_price=self.data_factory.random_number(digits=2),
            currency_price=self.data_factory.random_element(
                [currency.value for currency in CURRENCY_PRODUCT]),
            is_promotion=self.data_factory.boolean(),
            discount_price=self.data_factory.random_number(digits=2),
            expired_at=self.data_factory.date_time(),
            url_photo=self.data_factory.image_url(),
            store_conditions=self.data_factory.text()
        )
        ProductRepository.create_massive_products(self.process_id, [product])
        
        result = ProductRepository.create_massive_products(self.process_id, [product])
        
        assert len(result) == 0