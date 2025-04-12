import uuid

from typing import Optional, Any
from uuid import UUID, uuid4

from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from ..config.db import db

from ..infrastructure.seller_sort_field import SellerSortField

from ..models.seller_model import Seller


class SellerRepository:
    def __init__(self, session: Session):
        self._session = session

    def create_seller(self, seller_data: dict) -> Seller:
        # Convert string UUIDs to UUID objects
        seller_data['id'] = uuid4()
        if isinstance(seller_data.get('user_id'), str):
            seller_data['user_id'] = UUID(seller_data['user_id'])

        seller = Seller(**seller_data)
        self._session.add(seller)
        self._session.flush()
        return seller

    def get_seller_by_id(self, seller_id: uuid.uuid4) -> Seller | None:
        return self._session.query(Seller).filter_by(id=seller_id).one_or_none()

    def get_seller_by_user_id(self, user_id: uuid.uuid4) -> Seller | None:
        return self._session.query(Seller).filter_by(user_id=user_id).one_or_none()

    def get_all_sellers(self) -> list[Seller]:
        return self._session.query(Seller).all()

    def get_seller_by_id_full(self, seller_id: str) -> Seller:
        return Seller.query.filter_by(id=seller_id).first()

    def get_sellers_paginated(self,
            page: int = 1,
            per_page: int = 10,
            sort_by: Optional[SellerSortField] = SellerSortField.NAME,
            sort_order: str = "asc") -> dict[str, int | list[Any] | Any]:
        """Get all clients for a specific seller"""
        # Validate sort order
        sort_fn = asc if sort_order.lower() == "asc" else desc

        # Map enum to actual model field
        sort_column = {
            SellerSortField.NAME: Seller.name,
            SellerSortField.ZONE: Seller.zone,
            SellerSortField.EMAIL: Seller.email
        }.get(sort_by, Seller.name)

        # Build and paginate query
        pagination = (
            Seller.query
            .order_by(sort_fn(sort_column))
            .paginate(page=page, per_page=per_page, error_out=False)
        )

        return {
            "data": [seller.to_dict() for seller in pagination.items],
            "total": pagination.total,
            "page": pagination.page,
            "total_pages": pagination.pages,
            "per_page": pagination.per_page
        }

    @staticmethod
    def clean_transactions() -> None:
        db.session.rollback()
