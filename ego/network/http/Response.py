from abc import ABCMeta
from abc import abstractmethod


class Response:
    __metaclass__ = ABCMeta

    def __init__(self, code):
        self.__code = code
        self.__headers = {}
        self.__encoding = "utf-8"
        self.__data = None

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, code):
        self.__code = code

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
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    @abstractmethod
    def get_json(self, *args, **kwargs):
        pass
