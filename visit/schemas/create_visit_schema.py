UUID_PATTERN = "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
DATETIME_PATTERN = "^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])\s(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d"

CREATE_VISIT_SCHEMA = {
    'type': 'object',
    'properties': {
        'client_id': {
            'type': 'string',
            'pattern': UUID_PATTERN,
            'minLength': 36,
            'maxLength': 36
        },
        'description': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 500
        },
        'visit_date': {
            'type': 'string',
            'format': 'date-time',
            'pattern': DATETIME_PATTERN,
            'minLength': 19,
            'maxLength': 19
        },
        'products': {
            'type': 'array',
            'minItems': 0,
            'items': {
                'type': 'object',
                'properties': {
                    'product_id': {
                        'type': 'string',
                        'pattern': UUID_PATTERN,
                        'minLength': 36,
                        'maxLength': 36
                    },
                },
                'required': ['product_id'],
            },
        },
    },
    'required': ['client_id', 'description', 'visit_date', 'products'],
}
