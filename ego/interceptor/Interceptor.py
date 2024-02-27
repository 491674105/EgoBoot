

class Interceptor(object):
    order_id = -1

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

    def pre_handle(self):
        return True

    def post_handle(self):
        return True

    def after_completion(self):
        return True
