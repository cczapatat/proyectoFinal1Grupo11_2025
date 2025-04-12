import uuid
from datetime import datetime

from ..models.enums import STATE

from ..config.db import db
from ..dtos.store_in_dto import StoreInDTO
from ..models.store_model import Store

from sqlalchemy import asc, desc


class StoreRepository:
    @staticmethod
    def get_store_by_id(id_store: uuid.uuid4) -> Store | None:
        store = db.session.query(Store).filter_by(id=id_store).one_or_none()

        return store

    @staticmethod
    def create_store(store_in_dto: StoreInDTO) -> Store:
        store = Store()
        store.name = store_in_dto.name
        store.phone = store_in_dto.phone
        store.email = store_in_dto.email
        store.address = store_in_dto.address
        store.capacity = store_in_dto.capacity
        store.state = store_in_dto.state
        store.security_level = store_in_dto.security_level
        store.created_at = datetime.now()
        store.updated_at = datetime.now()

        db.session.add(store)
        db.session.commit()

        return store

    @staticmethod
    def get_stores_by_page(page: int, per_page: int, state : STATE) -> list[Store]: 
        offset = (page - 1) * per_page
        stores = db.session.query(Store).filter_by(state=state).order_by(Store.name).offset(offset).limit(per_page).all()

        return stores
    
    @staticmethod
    def get_stores_paginated_full(page: int = 1, per_page: int = 10, sort_order: str = "asc") -> dict:  
        # Validar orden de clasificación: usar función asc o desc
        sort_fn = asc if sort_order.lower() == "asc" else desc

        # Se ordena por el nombre de la tienda por defecto
        sort_column = Store.name

        # Construir y paginar la consulta. Se utiliza error_out=False para evitar levantar excepciones si la página no existe.
        pagination = Store.query.order_by(sort_fn(sort_column)).paginate(page=page, per_page=per_page, error_out=False)

        return {
            "data": [store.to_dict() for store in pagination.items],
            "total": pagination.total,
            "page": pagination.page,
            "total_pages": pagination.pages,
            "per_page": pagination.per_page
        }
