class ApiException(Exception):
    pass


class ObjectNotFoundError(ApiException):
    pass


class ObjectAlreadyExistError(ApiException):
    pass


class InvalidUrlError(ApiException):
    pass
