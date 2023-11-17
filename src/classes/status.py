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