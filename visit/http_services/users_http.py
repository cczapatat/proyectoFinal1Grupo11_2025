import os
import uuid

import requests
from werkzeug.exceptions import NotFound

internal_token = os.getenv('INTERNAL_TOKEN', default='internal_token')
sellers_path = os.getenv('SELLERS_PATH', default='http://localhost:3007')
clients_path = os.getenv('CLIENTS_PATH', default='http://localhost:3009')


def get_seller_by_id(seller_id: uuid) -> dict:
    seller_response = requests.get(f'{sellers_path}/sellers/by-id/{seller_id}', headers={
        'x-token': internal_token,
    })

    if seller_response.status_code != 200:
        raise NotFound(description='seller not found')

    return seller_response.json()


def get_client_by_id(client_id: uuid, seller_id: uuid) -> dict:
    client_response = requests.get(f'{clients_path}/clients/client-id/{client_id}/seller-id/{seller_id}', headers={
        'x-token': internal_token,
    })

    if client_response.status_code != 200:
        raise NotFound(description='client not found')

    return client_response.json()
