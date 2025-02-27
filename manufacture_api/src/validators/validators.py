from errors.errors import BadRequest
from jsonschema import validate
import jsonschema
import traceback

SchemaBulkTask = {
    "type": "object",
    "properties": {
        "user_email": {"type": "string", "format": "email"},
        "file_id": {"type": "string", "minLength": 1, "maxLength": 256},
    },
    "required": ["file_id", "user_email"]
}

def validate_schema(json_data, schema):
    try:
        validate(instance=json_data, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        traceback.print_exc()
        raise BadRequest(f"Invalid data: {e.message}")
    
def validate_token(headers):
    #TODO: Implement token validation
    pass