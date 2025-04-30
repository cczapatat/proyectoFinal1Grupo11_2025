import uuid

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
