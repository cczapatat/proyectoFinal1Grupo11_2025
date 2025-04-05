from ..models.enums import PAYMENT_METHOD

UUID_PATTERN = "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
DATETIME_PATTERN = "^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])\s(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d"

CREATE_ORDER_SCHEMA = {
    'type': 'object',
    'properties': {
        'seller_id': {
            'type': 'string',
            'pattern': UUID_PATTERN,
            'minLength': 36,
            'maxLength': 36
        },
        'client_id': {
            'type': 'string',
            'pattern': UUID_PATTERN,
            'minLength': 36,
            'maxLength': 36
        },
        'delivery_date': {
            'type': 'string',
            'format': 'date-time',
            'pattern': DATETIME_PATTERN,
            'minLength': 19,
            'maxLength': 19
        },
        'payment_method': {'type': 'string', 'enum': [method.name for method in PAYMENT_METHOD]},
        'products': {
            'type': 'array',
            'minItems': 1,
            'items': {
                'type': 'object',
                'properties': {
                    'product_id': {
                        'type': 'string',
                        'pattern': UUID_PATTERN,
                        'minLength': 36,
                        'maxLength': 36
                    },
                    'units': {'type': 'integer', 'minimum': 1},
                },
                'required': ['product_id', 'units'],
            },
        },
    },
    'required': ['client_id', 'delivery_date', 'payment_method', 'products'],
}
