import os

import requests

internal_token = os.getenv('INTERNAL_TOKEN', default='internal_token')
visits_path = os.getenv('VISITS_PATH', default='http://localhost:3020')


def create_visit(visit_data: dict, token: str) -> [int, dict]:
    visit_response = requests.post(
        f'{visits_path}/visits/create',
        headers={
            'x-token': internal_token,
            'Authorization': token,
        },
        json=visit_data,
    )

    return [visit_response.status_code, visit_response.json()]
