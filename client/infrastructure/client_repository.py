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

        #Check if the client_id alredy exists
        existing_client = Client.query.filter(
            (Client.email == client_dto.email) | (Client.phone == client_dto.phone)
        ).first()
        if existing_client:
            #return error if the client already exists
            return make_response(
                jsonify({"error": "Client already exists", "message": "Client already exists"}), 400
            )

        print(f"Creating client with email {client_dto.email} and phone {client_dto.phone}")
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
    def get_client_by_user_id_with_seller(user_id: int):
        client = Client.query.filter_by(user_id=user_id).first()

        if client:
            return get_client_with_seller(client.id)
        return None

    @staticmethod
    def clean_transactions() -> None:
        db.session.rollback()

def get_clients_by_seller_id(seller_id):
    """Get all clients for a specific seller"""
    clients = db.session.query(Client). \
        join(ClientSeller, Client.id == ClientSeller.client_id). \
        filter(ClientSeller.seller_id == seller_id). \
        all()

    return [client.to_dict() for client in clients]

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