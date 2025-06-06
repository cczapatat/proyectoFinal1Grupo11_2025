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

def get_all_visits_by_date(visit_date: str, token: str) -> [int, dict]:
    visit_response = requests.get(
        f'{visits_path}/visits/by-visit-date/{visit_date}',
        headers={
            'x-token': internal_token,
            'Authorization': token,
        },
    )

    return [visit_response.status_code, visit_response.json()]

def get_all_visits_by_date_paginated(visit_date: str, page: int, per_page: int, token: str) -> [int, dict]:
    visit_response = requests.get(
        f'{visits_path}/visits/by-visit-date-paginated/{visit_date}?page={page}&per_page={per_page}',
        headers={
            'x-token': internal_token,
            'Authorization': token,
        },
    )

    return [visit_response.status_code, visit_response.json()]
