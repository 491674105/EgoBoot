from ego.exception.default.CustomException import CustomException


class ShellException(CustomException):
    def __init__(self, msg):
        super(ShellException, self).__init__(msg)
