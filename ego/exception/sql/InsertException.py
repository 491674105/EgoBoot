from ego.exception.default.CustomException import CustomException


class InsertException(CustomException):
    def __init__(self, msg):
        super(InsertException, self).__init__(msg)
