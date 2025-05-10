UUID_PATTERN = "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
DATETIME_PATTERN = "^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])\s(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d"

CREATE_ALARM_SCHEMA = {
    'type': 'object',
    'properties': {
        'manufacture_id': {
            'type': 'string',
            'pattern': UUID_PATTERN,
            'minLength': 36,
            'maxLength': 36
        },
        'product_id': {
            'type': 'string',
            'pattern': UUID_PATTERN,
            'minLength': 36,
            'maxLength': 36
        },
        'minimum_value': {
            'type': 'integer',
            'minimum': 1
        },
        'maximum_value': {
            'type': 'integer',
            'minimum': 1
        },
        'notes': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 500
        },
    },
    'required': ['manufacture_id', 'product_id', 'notes'],
}
