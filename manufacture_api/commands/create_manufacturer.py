import traceback
import uuid
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from .base_command import BaseCommand
from ..errors.errors import ApiError
from ..models.Models import Manufacturer, db


class CreateManufacturer(BaseCommand):
    def __init__(self, name, address, phone, email, country, tax_conditions, legal_conditions, rating_quality):
        self.id = uuid.uuid4()
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.rating_quality = rating_quality
        self.country = country
        self.tax_conditions = tax_conditions
        self.legal_conditions = legal_conditions
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()

    def execute(self):
        try:
            new_manufacturer = Manufacturer(
                id=self.id,
                name=self.name,
                address=self.address,
                phone=self.phone,
                email=self.email,
                rating_quality=self.rating_quality,
                country=self.country,
                tax_conditions=self.tax_conditions,
                legal_conditions=self.legal_conditions,
                created_at=self.createdAt,
                updated_at=self.updatedAt
            )
            db.session.add(new_manufacturer)
            db.session.commit()

            return new_manufacturer.to_dict()

        except SQLAlchemyError as e:
            db.session.rollback()
            traceback.print_exc()
            raise ApiError(e)
