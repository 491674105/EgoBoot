from enum import Enum, unique


@unique
class ResultCode(Enum):
    # 10X
    CONTINUE = 100

    # 20X
    OK = 200
    PARTIAL_CONTENT = 206

    # 30X
    MULTIPLE_CHOICES = 300

    # 40X
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404

    # 50X
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
