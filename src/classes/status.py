from enum import IntEnum


class Status(IntEnum):
    """
    Class to define status codes for use with the OKException class.
    By default `status : 0` should be included with all API requests.
    """
    @staticmethod
    def dict(status: IntEnum, data=None) -> dict:
        if data is None:
            return {
                'status': status
            }
        data['status'] = status
        return data

    # Global Success Code
    SUCCESS = 0

    # Database Codes
    USER_NOT_FOUND = 1000
    PASSWORD_CONFIRMATION_FAILED = 1001
    INCORRECT_PASSWORD = 1002
    INVALID_USERNAME_OR_EMAIL = 1003