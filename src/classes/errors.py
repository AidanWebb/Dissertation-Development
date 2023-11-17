from enum import IntEnum


class HTTPStatus(IntEnum):
    """
    Integer enumeration for HTTP Status codes.
    """
    OK = 200
    BadRequest = 400
    Unauthorized = 401
    Forbidden = 403
    NotFound = 404
    Internal = 500


class HTTPException(Exception):
    """
    Class to define a HTTP non 200 Exception.
    """
    http_status = None
    error = None
    description = None

    def __init__(self, http_status, error):
        """
        Constructor for the HTTPException class.
        :param error: String representing HTTP error.
        """
        super()
        self.http_status = http_status
        self.error = error


class OKException(Exception):
    """
    Class to define a 200 OK Exception for known recoverable errors.
    """
    status = None

    def __init__(self, status):
        super()
        self.status = status


class Unauthorized(HTTPException):
    """
    Class to define the HTTP 401 Unauthorized Exception.
    """
    def __init__(self, description):
        super().__init__(HTTPStatus.Unauthorized, "Unauthorized")
        self.description = description


class BadRequest(HTTPException):
    """
    Class to define the HTTP 400 Bad Request Exception.
    """
    def __init__(self, description):
        super().__init__(HTTPStatus.BadRequest, "Bad Request")
        self.description = description


class Forbidden(HTTPException):
    """
    Class to define the HTTP 403 Forbidden Exception.
    """
    def __init__(self, description):
        super().__init__(HTTPStatus.Forbidden, "Forbidden")
        self.description = description


class NotFound(HTTPException):
    """
    Class to define the HTTP 403 Forbidden Exception.
    """
    def __init__(self, description):
        super().__init__(HTTPStatus.NotFound, "Not Found")
        self.description = description