class AppError(Exception):
    pass


class NotFound(AppError):
    pass


class BadRequest(AppError):
    pass


class ServerError(AppError):
    pass


class UnprocessableEntity(AppError):
    pass


class Unauthorized(AppError):
    pass


class Forbidden(AppError):
    pass
