import os
from ..errors.errors import BadRequest
from jsonschema import validate
from werkzeug.exceptions import Unauthorized
import jsonschema
import traceback

internal_token = os.getenv('INTERNAL_TOKEN', default='internal_token')

SchemaBulkTask = {
    "type": "object",
    "properties": {
        "user_id": {"type": "string", "format": "uuid"},
        "file_id": {"type": "string", "minLength": 1, "maxLength": 256},
    },
    "required": ["file_id", "user_id"]
}


def validate_schema(json_data, schema):
    try:
        validate(instance=json_data, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        traceback.print_exc()
        raise BadRequest(f"Invalid data: {e.message}")
    

def validate_token(headers):
    token = headers.get('x-token', None)

    if token is None:
        raise Unauthorized(description='authorization required')

    if token != internal_token:
        raise Unauthorized(description='authorization required')
