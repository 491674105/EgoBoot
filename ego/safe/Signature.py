from abc import ABCMeta
from abc import abstractmethod

from enum import Enum, unique


@unique
class Algorithm(Enum):
    SHA1 = "SHA-1"
    SHA256 = "SHA-256"
    DES = "DES"
    AES = "AES"
    MD5 = "MD5"


class Signature:
    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def signing(self, *args, **kwargs):
        pass

    @abstractmethod
    def verifying(self, *args, **kwargs):
        pass
