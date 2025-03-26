STORE_SCHEMA = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string', 'minLength': 1, 'maxLength': 255},
        'phone': {'type': 'string', 'pattern': '^\d+$', 'maxLength': 50},
        'email': {'type': 'string', 'format': 'email', 'maxLength': 255},
        'address': {'type': 'string', 'minLength': 1, 'maxLength': 500},
        'capacity': {'type': 'integer', 'minimum': 1},
        'state': {'type': 'string', 'enum': ['ACTIVE', 'INACTIVE']},
        'security_level': {'type': 'string', 'enum': ['HIGH', 'MEDIUM', 'LOW']}
    },
    'required': ['name', 'phone', 'email', 'address', 'capacity', 'state', 'security_level']
}
