from functools import wraps

from threading import current_thread as get_current_thread

from ego import applicationContext
from ego.exception.type.NullPointException import NullPointException
from ego.response.Result import Result

from ego.common.enum.auth.UserPermissionType import UserPermissionType
from ego.entity.dto.auth.RedisUserDTO import RedisUserDTO


class UserSessionCoreService:
    @staticmethod
    def get_user_session_instance() -> RedisUserDTO:
        if not applicationContext:
            raise NullPointException("ApplicationContext is empty.")

        if not hasattr(applicationContext, "user_sessions") or not getattr(applicationContext, "user_sessions"):
            raise NullPointException("can not find the user_sessions instance.")

        user_sessions = getattr(applicationContext, "user_sessions")
        current_thread = get_current_thread()
        return user_sessions[current_thread.ident]

    @staticmethod
    def set_user_session_instance(user_info):
        current_thread = get_current_thread()
        applicationContext.user_sessions[current_thread.ident] = user_info


class Auth:
    def __call__(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            user_info = UserSessionCoreService.get_user_session_instance()
            if user_info.id is None:
                return Result.failed(msg="用户信息异常！")
            if user_info.groupId not in UserPermissionType.get_all_roles():
                return Result.failed(msg="操作未授权！")

            return func(*args, **kwargs)

        return wrapper


class SysAdminAuth(Auth):
    def __call__(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            user_info = UserSessionCoreService.get_user_session_instance()
            if user_info.id is None:
                return Result.failed(msg="用户信息异常！")
            if user_info.groupId not in UserPermissionType.get_sys_admin_roles():
                return Result.failed(msg="操作未授权！")

            return func(*args, **kwargs)

        return wrapper
