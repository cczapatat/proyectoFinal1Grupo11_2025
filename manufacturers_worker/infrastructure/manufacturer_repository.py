from sqlalchemy import or_
from ..dtos.manufacturer_dto import ManufacturerDTO
from ..models.manufacturer_model import Manufacturer
from ..models.declarative_base import session


class ManufacturerRepository:
    @staticmethod
    def create_massive_manufacturers(transaction_id:str, manufacturersDTO: list[ManufacturerDTO]) -> list[Manufacturer]:
        manufacturers = []

        for manufacturerDTO in manufacturersDTO:
            manufacturer = Manufacturer()
            manufacturer.name = manufacturerDTO.name
            manufacturer.address = manufacturerDTO.address
            manufacturer.phone = manufacturerDTO.phone
            manufacturer.email = manufacturerDTO.email
            manufacturer.country = manufacturerDTO.country
            manufacturer.tax_conditions = manufacturerDTO.tax_conditions
            manufacturer.legal_conditions = manufacturerDTO.legal_conditions
            manufacturer.rating_quality = manufacturerDTO.rating_quality

            
            manufacturers.append(manufacturer)
        
        try:
            session.bulk_save_objects(manufacturers)
            session.commit()
            return manufacturers
        except Exception as ex:
            session.rollback()
            print(f"[Create Massive Manufacturers] process_id: {transaction_id}, error: {ex}")
            return []
    
    @staticmethod
    def get_existing_manufacturers_by_email_or_phone(emails: list[str], phones: list[str]) -> list[Manufacturer]:
        try:
            existing_manufacturers = session.query(Manufacturer).filter(
                or_(Manufacturer.email.in_(emails), Manufacturer.phone.in_(phones))
            ).all()
            return existing_manufacturers
        except Exception as ex:
            print(f"[Get Existing Manufacturers] Error: {ex}")
            return []