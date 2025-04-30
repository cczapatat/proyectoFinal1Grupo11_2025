import uuid
from datetime import datetime

from ..config.db import db
from ..dtos.visit_product_in_dto import VisitProductInDTO
from ..models.visits_product_model import VisitProduct


class VisitProductRepository:

    @staticmethod
    def create_visit_products(visit_id: uuid, visit_product_dtos: list[VisitProductInDTO]) -> list[VisitProduct]:
        visit_products = []

        for visit_product_dto in visit_product_dtos:
            visit_product = VisitProduct()
            visit_product.visit_id = visit_id
            visit_product.product_id = visit_product_dto.product_id
            visit_product.created_at = datetime.now()
            visit_product.updated_at = datetime.now()

            db.session.add(visit_product)
            visit_products.append(visit_product)

        return visit_products
