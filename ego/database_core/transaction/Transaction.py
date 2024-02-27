from functools import wraps
from threading import current_thread as get_current_thread

from sqlalchemy.orm import sessionmaker

from ego import applicationContext
from ego.logger.service.LoggerCoreService import LoggerCoreService
from ego.common.constant.config import Base

log = None


class Transactional:

    def __init__(self, *args, **kwargs):
        self.ncalls = 0

        global log
        log = LoggerCoreService.get_logger_instance()

    def __call__(self, func):
        self.func = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            current_thread = get_current_thread()
            if not hasattr(applicationContext, "session"):
                log.debug(f"{func.__qualname__}后台操作session")
                setattr(applicationContext, "session", {current_thread.ident: {}})

            session_dict = getattr(applicationContext, "session")
            if current_thread.ident not in session_dict:
                log.debug(f"{func.__qualname__}后台操作session")
                applicationContext.session[current_thread.ident] = {}

            user_session = session_dict[current_thread.ident]
            if "sql_connect" not in user_session or not user_session["sql_connect"]:
                connect = getattr(applicationContext, Base.ENGINE_KEY).connect()

                applicationContext.session[current_thread.ident]["sql_connect"] = connect
            else:
                connect = user_session["sql_connect"]
            session_maker = sessionmaker()
            session_maker.configure(bind=connect)
            session = session_maker()

            try:
                result = self.func(*args, **kwargs)
                session.commit()
                return result
            except Exception as e:
                raise e

        return wrapper

    @staticmethod
    def rollback(e):
        if not hasattr(applicationContext, "session"):
            return

        session_dict = getattr(applicationContext, "session")
        current_thread = get_current_thread()
        if current_thread.ident not in session_dict:
            return

        user_session = session_dict[current_thread.ident]
        if "sql_connect" not in user_session or not user_session["sql_connect"]:
            return

        connect = user_session["sql_connect"]
        session_maker = sessionmaker()
        session_maker.configure(bind=connect)
        session = session_maker()

        if hasattr(e, "msg"):
            msg = e.msg
        else:
            msg = "操作异常！"
        log.error(msg)
        log.exception(e)

        session.rollback()
        connect.close()

        # 清空会话缓存
        if current_thread.ident in applicationContext.session:
            del applicationContext.session[current_thread.ident]
