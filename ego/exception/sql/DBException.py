from ego.exception.default.CustomException import CustomException


class DBException(CustomException):
    def __init__(self, msg):
        super(DBException, self).__init__(msg)
