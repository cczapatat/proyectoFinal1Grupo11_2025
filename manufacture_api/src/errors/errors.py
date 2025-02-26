class ApiError(Exception):
    code = 500
    description = "An internal server error occurred"


class MissingToken(ApiError):
    code = 403
    description = "The token is missing from the request header"


class InvalidToken(ApiError):
    code = 401
    description = "The token is invalid or expired"


class BadRequest(ApiError):
    code = 400
    description = "Bad request"