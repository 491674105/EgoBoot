from abc import ABCMeta
from abc import abstractmethod


class Constructor:
    __classmeta__ = ABCMeta

    @abstractmethod
    def constructor(self, *args, **kwargs):
        pass
