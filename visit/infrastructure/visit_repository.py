import uuid
from datetime import datetime

from ..config.db import db
from ..dtos.visit_in_dto import VisitInDTO
from ..models.visit_model import Visit


class VisitRepository:

    @staticmethod
    def create_visit(visit_id: uuid, visit_dto: VisitInDTO) -> Visit:
        visit = Visit()
        visit.id = visit_id,
        visit.user_id = visit_dto.user_id
        visit.seller_id = visit_dto.seller_id
        visit.client_id = visit_dto.client_id
        visit.description = visit_dto.description
        visit.visit_date = visit_dto.visit_date
        visit.created_at = datetime.now()
        visit.updated_at = datetime.now()

        db.session.add(visit)
        return visit
