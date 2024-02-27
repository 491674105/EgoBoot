from asyncio import run_coroutine_threadsafe

from ego import applicationContext
from ego.coroutine.service.LoopCoreService import LoopCoreService

from ego.service.LogService import LogService


class Filter(object):
    order_id = -1

    logService = LogService()

    def __init__(self, **kwargs):
        self.__app = None
        if "app" in kwargs:
            self.__app = kwargs["app"]

        self.__current_app = None
        if "current_app" in kwargs:
            self.__current_app = kwargs["current_app"]

        self.__request = None
        if "request" in kwargs:
            self.__request = kwargs["request"]
            if "X-Real-Ip" in self.__request.headers and self.__request.headers["X-Real-Ip"]:
                self.__host = self.__request.headers["X-Real-Ip"]
            else:
                self.__host = self.__request.remote_addr

        self.__session = None
        if "session" in kwargs:
            self.__session = kwargs["session"]

        self.__g = None
        if "g" in kwargs:
            self.__g = kwargs["g"]

        self.__current_thread = None
        if "current_thread" in kwargs:
            self.__current_thread = kwargs["current_thread"]
            setattr(applicationContext, "session", {self.__current_thread.ident: {}})

    @property
    def app(self):
        return self.__app

    @app.setter
    def app(self, app_):
        self.__app = app_

    @property
    def current_app(self):
        return self.__current_app

    @current_app.setter
    def current_app(self, current_app_):
        self.__current_app = current_app_

    @property
    def request(self):
        return self.__request

    @request.setter
    def request(self, request_):
        self.__request = request_

        if "X-Real-Ip" in self.__request.headers and self.__request.headers["X-Real-Ip"]:
            self.__host = self.__request.headers["X-Real-Ip"]
        else:
            self.__host = self.__request.remote_addr

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, host_):
        self.__host = host_

    @property
    def session(self):
        return self.__session

    @session.setter
    def session(self, session_):
        self.__session = session_

    @property
    def g(self):
        return self.__g

    @g.setter
    def g(self, g_):
        self.__g = g_

    @property
    def current_thread(self):
        return self.__current_thread

    @current_thread.setter
    def current_thread(self, current_thread_):
        if current_thread_ is None:
            return
        self.__current_thread = current_thread_

        setattr(applicationContext, "session", {self.__current_thread.ident: {}})

    def handle_access_log(self):
        run_coroutine_threadsafe(self.logService.save_filter_access_log(self), LoopCoreService.get_loop_instance())

    def do_filter(self):
        """
            header数据过滤
            g.user_info：请求用户信息
            g.params：请求参数集
        """
        return True

    def __del__(self):
        pass
