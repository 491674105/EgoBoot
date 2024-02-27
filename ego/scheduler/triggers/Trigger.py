from abc import ABCMeta
from abc import abstractmethod


class Trigger:
    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def from_crontab(self, *args, **kwargs):
        """
            使用cron表达式
        """
        pass

    @abstractmethod
    def from_date(self, *args, **kwargs):
        """
            使用date
        """
        pass

    @abstractmethod
    def from_datetime(self, *args, **kwargs):
        """
            使用datetime
        """
        pass
