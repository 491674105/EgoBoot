from abc import ABCMeta
from abc import abstractmethod


class Encryption:
    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def generate_key(self, *args, **kwargs):
        pass

    @abstractmethod
    def exec_encrypt(self, *args, **kwargs):
        pass

    @abstractmethod
    def exec_decrypt(self, *args, **kwargs):
        pass
