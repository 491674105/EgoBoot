from ego.common.enum.network.ResultCode import ResultCode


class CustomException(Exception):
    def __init__(self, msg_=None, code_=None):
        if msg_:
            self.__msg = msg_

        if code_:
            self.__code = code_
        else:
            self.__code = ResultCode.INTERNAL_SERVER_ERROR.value
        super().__init__(msg_, None)

    @property
    def msg(self):
        return self.__msg

    @msg.setter
    def msg(self, msg_):
        self.__msg = msg_

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, code_):
        self.__code = code_
