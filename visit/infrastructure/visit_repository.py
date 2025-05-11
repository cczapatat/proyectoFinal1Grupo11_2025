from typing import List
import uuid
from datetime import datetime

from sqlalchemy import cast, String
from werkzeug.exceptions import InternalServerError

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
    
    @staticmethod
    def get_all_visits_by_visit_date(visit_date: str) -> List[Visit]:
        try:
            visits = Visit.query.filter(Visit.visit_date.cast(String).contains(visit_date)).all()
            return visits
        except Exception as e:
            raise InternalServerError(description=f"Error querying visits by date: {str(e)}")
    
    @staticmethod
    def get_visits_by_date_paginated_full(
        visit_date: str, page: int = 1, per_page: int = 10, sort_order: str = 'asc'
    ) -> List[Visit]:
        try:
            query = Visit.query.filter(Visit.visit_date.cast(String).contains(visit_date))
            if sort_order == 'asc':
                query = query.order_by(Visit.visit_date.asc())
            else:
                query = query.order_by(Visit.visit_date.desc())
            
            paginated = query.paginate(page=page, per_page=per_page, error_out=False)
            return paginated
        except Exception as e:
            raise InternalServerError(description=f"Error querying visits: {str(e)}")
