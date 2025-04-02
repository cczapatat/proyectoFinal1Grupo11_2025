from flask import request, Blueprint, jsonify
from validators.validators import validate_token
from commands.create_manufacturer import CreateManufacturer
from commands.get_all_manufacturer import GetAllManufacturer
from models.Models import BulkTaskSchema

manufacturer_blueprint = Blueprint('manufacturers', __name__, url_prefix='/manufacture-api')
bulk_task_schema = BulkTaskSchema()

def get_json_data(keys):
    return {key: request.get_json()[key] for key in keys}

@manufacturer_blueprint.route('/manufacturers/create', methods=['POST'])
def create():
    validate_token(request.headers)

    data = get_json_data([
        'name',
        'address',
        'phone',
        'email',
        'country',
        'tax_conditions',
        'legal_conditions',
        'rating_quality',
        ])
    
    print(data)

    manufacturer = CreateManufacturer(**data)
    manufacturer_response = manufacturer.execute()
    return jsonify(manufacturer_response), 201

@manufacturer_blueprint.route('/manufacturers/all', methods=['GET'])
def get_all_manufacturer():
    validate_token(request.headers)
    get_all_manufacturers = GetAllManufacturer()
    get_all_manufacturers_response = get_all_manufacturers.execute()
    return jsonify(get_all_manufacturers_response), 200