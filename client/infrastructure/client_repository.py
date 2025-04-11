import uuid
from datetime import datetime
from typing import List, Optional, Any

from sqlalchemy import asc, desc

from .client_sort_field import ClientSortField
from ..config.db import db
from ..dtos.client_dto import ClientDTO
from ..models import ClientSeller
from ..models.client_model import Client


class ClientRepository:

    @staticmethod
    def create_client(client_dto: ClientDTO) -> (Client,str):
        client = Client()
        client.user_id = client_dto.user_id
        client.name = client_dto.name
        client.phone = client_dto.phone
        client.email = client_dto.email
        client.address = client_dto.address
        client.client_type = client_dto.client_type
        client.zone = client_dto.zone
        client.created_at = datetime.now()
        client.updated_at = datetime.now()

        db.session.add(client)
        db.session.flush()

        if client_dto.seller_id is not None:
            client_seller = ClientSeller(
                client_id=client.id,
                seller_id=client_dto.seller_id
            )
            db.session.add(client_seller)

        db.session.commit()

        return client,client_dto.seller_id

    @staticmethod
    def get_client_by_user_id(user_id: str) -> Client:
        return Client.query.filter_by(user_id=user_id).first()

    @staticmethod
    def get_client_by_user_id_with_seller(user_id: int):
        client = Client.query.filter_by(user_id=user_id).first()

        if client:
            return get_client_with_seller(client.id)
        return None

    @staticmethod
    def get_client_relation_seller(client_id: uuid.uuid4, seller_id: uuid.uuid4) -> Client | None:
        return db.session.query(Client). \
            join(ClientSeller, Client.id == ClientSeller.client_id). \
            filter(Client.id == client_id, ClientSeller.seller_id == seller_id). \
            one_or_none()

    @staticmethod
    def clean_transactions() -> None:
        db.session.rollback()

    @staticmethod
    def associate_seller(client_ids:List[str], seller_id):
        # Check if client already has a seller association
        associations = []

        # Process each client
        for client_id in client_ids:
            # Check if client already has a seller association
            existing_association = ClientSeller.query.filter_by(client_id=client_id).first()

            if existing_association:
                if existing_association.seller_id == seller_id:
                    # Update existing association if it's a different seller
                    associations.append(existing_association)
                    continue
                else:
                    # If it's a different seller, update the existing association
                    existing_association.seller_id = seller_id
                    db.session.commit()
                    associations.append(existing_association)
                    continue

            # Create new association
            new_association = ClientSeller(
                client_id=client_id,
                seller_id=seller_id,
            )
            db.session.add(new_association)
            associations.append(new_association)

        db.session.commit()
        db.session.flush()

        return get_clients_by_seller_id_paginated(seller_id)

    @staticmethod
    def get_client_by_id(client_id: str) -> Client:
        return Client.query.filter_by(id=client_id).first()

    @staticmethod
    def get_clients_by_ids(client_ids: List[str]) -> (List[Client], List[str]):
        if not client_ids:
            return [], []

            # Query all clients that match the provided IDs
        found_clients = Client.query.filter(Client.id.in_(client_ids)).all()

        # Create set of found client IDs

        # Find missing client IDs by comparing with input IDs
        missing_client_ids = len(client_ids) - len(found_clients)

        return found_clients, missing_client_ids


def get_clients_by_seller_id(seller_id):
    """Get all clients for a specific seller"""
    clients = db.session.query(Client). \
        join(ClientSeller, Client.id == ClientSeller.client_id). \
        filter(ClientSeller.seller_id == seller_id). \
        all()

    return [client.to_dict() for client in clients]

def get_clients_by_seller_id_paginated(
        seller_id: int,
        page: int = 1,
        per_page: int = 10,
        sort_by: Optional[ClientSortField] = ClientSortField.NAME,
        sort_order: str = "asc") -> dict[str, int | list[Any] | Any]:
    """Get all clients for a specific seller"""
    # Validate sort order
    sort_fn = asc if sort_order.lower() == "asc" else desc

    # Map enum to actual model field
    sort_column = {
        ClientSortField.NAME: Client.name,
        ClientSortField.ZONE: Client.zone,
        ClientSortField.EMAIL: Client.email
    }.get(sort_by, Client.name)

    # Build base query
    query = (
        db.session.query(Client)
        .join(ClientSeller, Client.id == ClientSeller.client_id)
        .filter(ClientSeller.seller_id == seller_id)
    )

    # Get total count before pagination
    total = query.count()

    # Apply sorting, pagination
    clients = (
        query
        .order_by(sort_fn(sort_column))
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return {
        "data": [client.to_dict() for client in clients],
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page  # ceil
    }

def get_client_with_seller(client_id):
    """Helper function to get client with seller information"""

    result = db.session.query(Client, ClientSeller). \
        join(ClientSeller, Client.id == ClientSeller.client_id). \
        filter(Client.id == client_id). \
        first()

    if result:
        client, client_seller = result
        temp_client = client.to_dict()

        return {
            'id': client.id,
            'user_id': client.user_id,
            'name': client.name,
            'phone': client.phone,
            'email': client.email,
            'address': client.address,
            'client_type': temp_client['client_type'],
            'zone': temp_client['zone'],
            'created_at': client.created_at,
            'updated_at': client.updated_at,
            'seller_id': client_seller.seller_id
        }
    return None
