from abc import ABCMeta
from abc import abstractmethod


class Client(object):
    __metaclass__ = ABCMeta

    def __init__(self, host=None, port=80, timeout=30, use_ssl=False):
        if host:
            self.__host = host
        self.__port = port
        self.__timeout = timeout

        self.__use_ssl = use_ssl

        self.__headers = {}

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, host):
        self.__host = host

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port):
        self.__port = port

    @property
    def timeout(self):
        return self.__timeout

    @timeout.setter
    def timeout(self, timeout):
        self.__timeout = timeout

    @property
    def use_ssl(self):
        return self.__use_ssl

    @use_ssl.setter
    def use_ssl(self, use_ssl):
        self.__use_ssl = use_ssl

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, headers):
        for key in headers:
            self.__headers[key] = headers[key]

    @abstractmethod
    def open_original_request(self, method, url, params=None, headers=None, body=None, *args, **kwargs):
        pass

    @abstractmethod
    def open_request(self, method, uri, params=None, headers=None, body=None, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, uri, params=None, headers=None, *args, **kwargs):
        pass

    @abstractmethod
    def post(self, uri, params=None, headers=None, body=None, *args, **kwargs):
        pass

    @abstractmethod
    def put(self, uri, headers=None, body=None, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, uri, headers=None, *args, **kwargs):
        pass
