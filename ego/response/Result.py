from ego.common.enum.network.ResultCode import ResultCode


class Result(object):
    code = ResultCode.OK.value
    msg = ResultCode.OK.name
    data = {}

    def __init__(self, code=None, msg=None, data=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        if data is not None:
            self.data = data

    def body(self):
        body = {
            "code": self.code,
            "msg": self.msg,
            "data": self.data
        }
        return body

    @classmethod
    def success(cls, code=None, msg=None, data=None):
        if code:
            return cls(code, msg, data).body()
        return cls(ResultCode.OK.value, msg, data).body()

    @classmethod
    def success_default(cls, data=None):
        return cls(ResultCode.OK.value, ResultCode.OK.name, data).body()

    @classmethod
    def failed(cls, code=None, msg=None, data=None):
        if code:
            return cls(code, msg, data).body()
        return cls(ResultCode.INTERNAL_SERVER_ERROR.value, msg, data).body()

    @classmethod
    def not_found(cls, code=ResultCode.NOT_FOUND.value, msg=ResultCode.NOT_FOUND.name, data=None):
        return cls(code, msg, data).body()

    @classmethod
    def failed_default(cls, data=None):
        return cls(
            ResultCode.INTERNAL_SERVER_ERROR.value,
            ResultCode.INTERNAL_SERVER_ERROR.name,
            data
        ).body()
