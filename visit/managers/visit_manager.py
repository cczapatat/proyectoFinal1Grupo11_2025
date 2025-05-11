from typing import List
import uuid

from werkzeug.exceptions import InternalServerError

from ..dtos.client_in_dto import ClientInDTO
from ..dtos.extended_visit_in_dto import ExtendedVisitInDTO

from ..dtos.visit_in_dto import VisitInDTO
from ..http_services.users_http import get_seller_by_id, get_client_by_id
from ..infrastructure.visit_product_repository import VisitProductRepository
from ..infrastructure.visit_repository import VisitRepository
from ..infrastructure.transaction import Transaction
from ..models.visit_model import Visit
from ..models.visits_product_model import VisitProduct


class VisitManager:
    def __init__(self):
        self.visit_repository = VisitRepository()
        self.visit_product_repository = VisitProductRepository()
        self.transaction = Transaction()

    def create_visit(self, visit_in_dto: VisitInDTO) -> dict:
        get_seller_by_id(visit_in_dto.seller_id)
        get_client_by_id(visit_in_dto.client_id, visit_in_dto.seller_id)

        def transaction_operations() -> [Visit, VisitProduct]:
            visit_id = uuid.uuid4()
            visit_internal = self.visit_repository.create_visit(visit_id, visit_in_dto)
            products_internal = self.visit_product_repository.create_visit_products(visit_id, visit_in_dto.products)
            return [visit_internal, products_internal]

        [visit, products] = self.transaction.run(transaction_operations)

        return visit.to_dict(products)
    

    def get_all_visits_by_date_paginated_full(
        self, visit_date: str, page: int = 1, per_page: int = 10, sort_order: str = 'asc'
    ) -> dict:
        try:
            # Fetch paginated visits from the repository
            paginated = self.visit_repository.get_visits_by_date_paginated_full(
                visit_date, page=page, per_page=per_page, sort_order=sort_order
            )

            # Transform visits into a list of dictionaries
            visits = [
                {
                    'id': str(visit.id),
                    'user_id': visit.user_id,
                    'seller_id': visit.seller_id,
                    'client': self.__get_client_by_id(visit.client_id, visit.seller_id),
                    'description': visit.description,
                    'visit_date': visit.visit_date.strftime('%Y-%m-%d %H:%M:%S'),
                }
                for visit in paginated.items
            ]

            # Return paginated response
            return {
                'data': visits,
                'total': paginated.total,
                'page': paginated.page,
                'per_page': paginated.per_page,
                'total_pages': paginated.pages,
            }

        except Exception as e:
            # Raise an internal server error with a descriptive message
            raise InternalServerError(description=f"Error retrieving visits: {str(e)}")


    def get_all_visits_by_visit_date(self, visit_date: str):
        try:
            # Ensure visit_date is compared as a date, not as a string
            visits = self.visit_repository.get_all_visits_by_visit_date(visit_date)
            return [
                {
                    'id': str(visit.id),
                    'user_id': visit.user_id,
                    'seller_id': visit.seller_id,
                    'client': self.__get_client_by_id(visit.client_id, visit.seller_id), 
                    'description': visit.description,
                    'visit_date': visit.visit_date.strftime('%Y-%m-%d %H:%M:%S'),
                    
                } for visit in visits
            ]
        except Exception as e:
            raise InternalServerError(description=f"Error retrieving visits: {str(e)}")

    def __get_client_by_id(self, client_id: uuid.UUID, seller_id: uuid.UUID) -> ClientInDTO:
        client_data = get_client_by_id(client_id, seller_id)
        client_dto = ClientInDTO(
            id=client_data["id"],
            name=client_data["name"],
            zone=client_data["zone"],
            client_type=client_data["client_type"],
        )
        return client_dto
