import os
import uuid

import requests
from werkzeug.exceptions import NotFound

internal_token = os.getenv('INTERNAL_TOKEN', default='internal_token')
products_path = os.getenv('PRODUCTS_PATH', default='http://localhost:3017')


def get_products_by_id(products_id: list[uuid]) -> dict:
    product_response = requests.post(
        f'{products_path}/products/by-ids',
        headers={'x-token': internal_token},
        json={"ids": products_id}
    )

    if product_response.status_code != 200:
        raise NotFound(description='products not found')

    return product_response.json()
