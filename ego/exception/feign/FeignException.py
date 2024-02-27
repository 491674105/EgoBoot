from ego.exception.default.CustomException import CustomException


class FeignException(CustomException):
    def __init__(self, msg):
        super(FeignException, self).__init__(msg)
