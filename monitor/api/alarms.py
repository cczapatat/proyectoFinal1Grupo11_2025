import os
import uuid

import requests
from flask import Blueprint, jsonify, request
from flask_validate_json import validate_json
from sqlalchemy.exc import DataError
from werkzeug.exceptions import Unauthorized, InternalServerError

from ..dtos.alarm_in_dto import AlarmInDTO
from ..managers.alarm_manager import AlarmManager
from ..schemas.create_alarm_schema import CREATE_ALARM_SCHEMA

bp = Blueprint('monitor', __name__, url_prefix='/monitor')

internal_token = os.getenv('INTERNAL_TOKEN', default='internal_token')
user_session_manager_path = os.getenv('USER_SESSION_MANAGER_PATH', default='http://localhost:3008')

alarm_manager = AlarmManager()


def __there_is_token() -> None:
    token = request.headers.get('x-token', None)

    if token is None or token != internal_token:
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


def __dict_to_alarm_in_dto(user_id: uuid, data: dict) -> AlarmInDTO:
    return AlarmInDTO(
        user_id=user_id,
        manufacture_id=data.get('manufacture_id'),
        product_id=data.get('product_id'),
        minimum_value=data.get('minimum_value', None),
        maximum_value=data.get('maximum_value', None),
        notes=data.get('notes')
    )


@bp.route('/new', methods=('POST',))
@validate_json(CREATE_ALARM_SCHEMA)
def create_order():
    __there_is_token()
    user_auth = __validate_auth_token()

    user_id = user_auth['user_session_id']

    request_data = request.get_json()
    alarm_in_dto = __dict_to_alarm_in_dto(user_id, request_data)

    if alarm_in_dto.minimum_value is None and alarm_in_dto.maximum_value is None:
        return jsonify({'message': 'minimum_value or maximum_value is required'}), 400

    alarm_created = alarm_manager.create_alarm(alarm_in_dto)

    return jsonify(alarm_created), 201


@bp.errorhandler(400)
@bp.errorhandler(401)
@bp.errorhandler(404)
@bp.errorhandler(500)
def handle_validation_error(error):
    return jsonify({
        'message': str(error.description)
    }), error.code


@bp.errorhandler(DataError)
def handle_integrity_error(error):
    return jsonify({
        'message': f'Database integrity error. {str(error.code)}'
    }), 409
