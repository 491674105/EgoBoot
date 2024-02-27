from ego.exception.default.CustomException import CustomException


class NumberTransException(CustomException):
    def __init__(self, msg_):
        super(NumberTransException, self).__init__(msg_)
