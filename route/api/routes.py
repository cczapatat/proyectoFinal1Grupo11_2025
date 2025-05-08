import os

import requests
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import Unauthorized, InternalServerError

from ..http_services.visit_http import create_visit, get_all_visits_by_date

bp = Blueprint('routes', __name__, url_prefix='/routes')

internal_token = os.getenv('INTERNAL_TOKEN', default='internal_token')
user_session_manager_path = os.getenv('USER_SESSION_MANAGER_PATH', default='http://localhost:3008')


def __there_is_token() -> None:
    token = request.headers.get('x-token', None)

    if token is None:
        raise Unauthorized(description='x-token required')

    if token != internal_token:
        raise Unauthorized(description='x-token required')


def __validate_auth_token() -> dict:
    auth_token = request.headers.get('Authorization', None)

    if auth_token is None:
        raise Unauthorized(description='authorization required')

    auth_response = requests.get(f'{user_session_manager_path}/user_sessions/auth', headers={
        'Authorization': auth_token,
    })

    if auth_response.status_code == 401:
        raise Unauthorized(description='authorization required')
    elif auth_response.status_code != 200:
        raise InternalServerError(description='internal server error on user_session_manager')

    return auth_response.json()


@bp.route('/visits/create', methods=('POST',))
def create_order():
    __there_is_token()
    __validate_auth_token()

    [status_code, visit_created] = create_visit(request.get_json(), request.headers.get('Authorization'))

    return jsonify(visit_created), status_code

@bp.route('/visits/get_by_visit_date', methods=('GET',))
def get_all_visits_by_visit_date():
    __there_is_token()
    __validate_auth_token()

    visit_date = request.args.get('visit_date')

    if not visit_date:
        raise Unauthorized(description='visit_date required')

    [status_code, visits] = get_all_visits_by_date(visit_date, request.headers.get('Authorization'))

    return jsonify(visits), status_code


@bp.errorhandler(400)
@bp.errorhandler(401)
@bp.errorhandler(404)
@bp.errorhandler(500)
def handle_validation_error(error):
    return jsonify({
        'message': str(error.description)
    }), error.code
