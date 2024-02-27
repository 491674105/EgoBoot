from abc import ABCMeta
from abc import abstractmethod


class Request:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.__headers = {}
        self.__encoding = "utf-8"
        self.__body = {}

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, headers):
        self.__headers = headers

    @property
    def encoding(self):
        return self.__encoding

    @encoding.setter
    def encoding(self, encoding):
        self.__encoding = encoding

    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, body):
        self.__body = body

    @abstractmethod
    def sign(self, *args, **kwargs):
        pass
