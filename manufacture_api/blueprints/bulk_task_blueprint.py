from flask import request, Blueprint, jsonify
from ..validators.validators import validate_token
from ..commands.create_command import CreateBulkTask
from ..commands.reset import ResetBulkTask
from ..models.Models import BulkTaskSchema

bulk_task_blueprint = Blueprint('bulk_task', __name__, url_prefix='/manufacture-api')
bulk_task_schema = BulkTaskSchema()

def get_json_data(keys):
    return {key: request.get_json()[key] for key in keys}

@bulk_task_blueprint.route('/bulk', methods=['POST'])
def create():
    validate_token(request.headers)
    data = get_json_data(['user_id', 'file_id'])
    bulk_task = CreateBulkTask(**data)
    creation_response = bulk_task.execute()
    return jsonify(creation_response), 201

@bulk_task_blueprint.route('/bulk/ping', methods=['GET'])
def health():
    return "pong", 200

@bulk_task_blueprint.route('/bulk/reset', methods=['POST'])
def reset():
    ResetBulkTask().execute()
    return jsonify({'msg': 'Todos los datos fueron eliminados'}), 200
