from functools import wraps
from threading import current_thread as get_current_thread

from ego import applicationContext

from ego.exception.api.APIException import APIException

log = applicationContext.log


class Auth:

    def __init__(self, *args, **kwargs):
        self.ncalls = 0

    def __call__(self, func):
        self.func = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            current_thread = get_current_thread()

            if not hasattr(applicationContext, "user_sessions"):
                raise APIException("请登录！")

            if current_thread.ident not in applicationContext.user_sessions:
                raise APIException("操作未授权！")

            user_info = applicationContext.user_sessions[current_thread.ident]
            if user_info.id is None:
                raise APIException("用户信息异常！")

            return func(*args, **kwargs)

        return wrapper
