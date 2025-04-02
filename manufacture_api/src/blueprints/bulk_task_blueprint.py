from flask import request, Blueprint, jsonify
from validators.validators import validate_token
from commands.create_command import CreateBulkTask
from commands.update_command import BulkTaskUpdate
from commands.filter_command import FilterBulkTaskByUserEmail, FilterBulkTaskById
from commands.reset import ResetBulkTask
from models.Models import BulkTaskSchema

bulk_task_blueprint = Blueprint('bulk_task', __name__, url_prefix='/manufacture-api')
bulk_task_schema = BulkTaskSchema()

def get_json_data(keys):
    return {key: request.get_json()[key] for key in keys}

@bulk_task_blueprint.route('/bulk', methods=['POST'])
def create():
    validate_token(request.headers)
    data = get_json_data(['user_email', 'file_id'])
    bulk_task = CreateBulkTask(**data)
    creation_response = bulk_task.execute()
    return jsonify(creation_response), 201

@bulk_task_blueprint.route('/bulk', methods=['GET'])
def get_by_user():
    validate_token(request.headers)
    filter_by_user = FilterBulkTaskById(id=request.args.get('id'))
    filtered_bulk_task = filter_by_user.execute()
    return jsonify(bulk_task_schema.dump(filtered_bulk_task)), 200

@bulk_task_blueprint.route('/bulk/user', methods=['GET'])
def get_by_status():
    filter_by_email = FilterBulkTaskByUserEmail(user_email=request.args.get('user_email'))
    filtered_bulk_tasks = filter_by_email.execute()
    return jsonify([bulk_task_schema.dump(task) for task in filtered_bulk_tasks]), 200

@bulk_task_blueprint.route('/bulk/update', methods=['POST'])
def update():
    data = get_json_data(['id', 'status'])
    card_to_update = BulkTaskUpdate(**data)
    card = card_to_update.execute()
    return jsonify(bulk_task_schema.dump(card)), 200

@bulk_task_blueprint.route('/bulk/ping', methods=['GET'])
def health():
    return "pong", 200

@bulk_task_blueprint.route('/bulk/reset', methods=['POST'])
def reset():
    ResetBulkTask().execute()
    return jsonify({'msg': 'Todos los datos fueron eliminados'}), 200
