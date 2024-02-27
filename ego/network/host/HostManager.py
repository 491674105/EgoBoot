

from abc import ABCMeta
from abc import abstractmethod


class AbstractHostManager(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def check_hosts(self, *args, **kwargs):
        pass
