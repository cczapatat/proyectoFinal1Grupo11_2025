from faker import Faker
from manufacturers_worker.dtos.manufacturer_dto import ManufacturerDTO
from manufacturers_worker.infrastructure.manufacturer_repository import ManufacturerRepository
from manufacturers_worker.models.manufacturer_model import Manufacturer, MANUFACTURER_COUNTRY
from manufacturers_worker.models.declarative_base import session
import manufacturers_worker.init_bd

class TestManufacturerRepository:
    def setup_method(self):
        self.data_factory = Faker()
        session.rollback()
        session.query(Manufacturer).delete()
        session.commit()
        self.process_id = str(self.data_factory.uuid4())
        


    def test_create_massive_manufacturers_success(self):
        manufacturers = []
        for _ in range(5):
            manufacturer = ManufacturerDTO(
                name=self.data_factory.name(),
                address=self.data_factory.address(),
                phone='+5730054367' + str(self.data_factory.random_int(min=1000, max=9999)),
                email=self.data_factory.email(),
                country= self.data_factory.random_element(
                [country for country in MANUFACTURER_COUNTRY]),
                tax_conditions=self.data_factory.text(),
                legal_conditions=self.data_factory.text(),
                rating_quality=self.data_factory.random_int(min=0, max=5),
            )
            manufacturers.append(manufacturer)
        
        result = ManufacturerRepository.create_massive_manufacturers(self.process_id, manufacturers)
        
        assert len(result) == len(manufacturers)
    
    def test_create_massive_manufacturers_empty_list(self):
        manufacturers = []
        result = ManufacturerRepository.create_massive_manufacturers(self.process_id, manufacturers)
        
        assert len(result) == 0

    def test_create_massive_manufacturers_integrity_error(self):
        manufacturer = ManufacturerDTO(
            name=self.data_factory.name(),
            address=self.data_factory.address(),
            phone='+5730054367' + str(self.data_factory.random_int(min=1000, max=9999)),
            email=self.data_factory.email(),
            country= self.data_factory.random_element(
            [country for country in MANUFACTURER_COUNTRY]),
            tax_conditions=self.data_factory.text(),
            legal_conditions=self.data_factory.text(),
            rating_quality=self.data_factory.random_int(min=0, max=5)
        )
        ManufacturerRepository.create_massive_manufacturers(self.process_id, [manufacturer])
        
        result = ManufacturerRepository.create_massive_manufacturers(self.process_id, [manufacturer])
        
        assert len(result) == 0
    
    def test_get_existing_manufacturers_by_email_or_phone_success(self):
        manufacturer = ManufacturerDTO(
            name=self.data_factory.name(),
            address=self.data_factory.address(),
            phone='+5730054367' + str(self.data_factory.random_int(min=1000, max=9999)),
            email=self.data_factory.email(),
            country= self.data_factory.random_element(
            [country for country in MANUFACTURER_COUNTRY]),
            tax_conditions=self.data_factory.text(),
            legal_conditions=self.data_factory.text(),
            rating_quality=self.data_factory.random_int(min=0, max=5)
        )
        ManufacturerRepository.create_massive_manufacturers(self.process_id, [manufacturer])
        
        result = ManufacturerRepository.get_existing_manufacturers_by_email_or_phone([manufacturer.email], [manufacturer.phone])
        
        assert len(result) == 1
        assert result[0].email == manufacturer.email
        assert result[0].phone == manufacturer.phone
    
    def test_get_existing_manufacturers_by_email_or_phone_empty_list(self):
        result = ManufacturerRepository.get_existing_manufacturers_by_email_or_phone([], [])
        
        assert len(result) == 0