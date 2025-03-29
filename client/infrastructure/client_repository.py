from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask import jsonify, make_response

from ..config.db import db
from ..models import ClientSeller
from ..models.client_model import Client
from ..dtos.client_dto import ClientDTO


class ClientRepository:

    @staticmethod
    def create_client(client_dto: ClientDTO) -> Client:
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

        client_seller = ClientSeller(
            client_id=client.id,
            seller_id=client_dto.seller_id
        )
        db.session.add(client_seller)
        db.session.commit()

        return client
    
    @staticmethod
    def get_client_by_user_id(user_id: int) -> Client:
        return Client.query.filter_by(user_id=user_id).first()

    @staticmethod
    def clean_transactions() -> None:
        db.session.rollback()


def get_client_with_seller(client_id):
    """Helper function to get client with seller information"""
    try:
        result = db.session.query(Client, ClientSeller). \
            join(ClientSeller, Client.id == ClientSeller.client_id). \
            filter(Client.id == client_id). \
            first()

        if result:
            client, client_seller = result
            return {
                'id': client.id,
                'user_id': client.user_id,
                'name': client.name,
                'phone': client.phone,
                'email': client.email,
                'address': client.address,
                'client_type': client.client_type,
                'zone': client.zone,
                'created_at': client.created_at,
                'updated_at': client.updated_at,
                'seller_id': client_seller.seller_id
            }
        return None
    except Exception as e:
        db.session.rollback()
        raise e