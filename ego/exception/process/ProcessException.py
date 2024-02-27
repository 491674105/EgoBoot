from ego.exception.default.CustomException import CustomException

from ego.common.enum.process.OpsProcessErrorLevel import OpsProcessErrorLevel


class ProcessException(CustomException):
    code = OpsProcessErrorLevel.FIRST.value
    msg = "sorry, we found a error!"

    def __init__(self, msg=None, code=None, step_id=None):
        if msg:
            self.msg = msg
        if code:
            self.code = code
        if step_id:
            self.step_id = step_id
        super().__init__(msg, code)


class ProcessQueryException(ProcessException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ProcessStartException(ProcessException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ProcessRollbackException(ProcessException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TaskQueryException(ProcessException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TaskClaimException(ProcessException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TaskCompleteException(ProcessException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
