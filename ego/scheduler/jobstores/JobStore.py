from abc import ABCMeta
from abc import abstractmethod


class JobStore:
    __metaclass__ = ABCMeta

    @abstractmethod
    def add_job(self, *args, **kwargs):
        """
            添加任务
        """
        pass

    @abstractmethod
    def add_jobs(self, *args, **kwargs):
        """
            批量添加任务
        """
        pass

    @abstractmethod
    def update_job(self, *args, **kwargs):
        """
            更新任务
        """
        pass

    @abstractmethod
    def update_jobs(self, *args, **kwargs):
        """
            批量更新任务
        """
        pass

    @abstractmethod
    def remove_job(self, *args, **kwargs):
        """
            删除任务
        """
        pass

    @abstractmethod
    def remove_jobs(self, *args, **kwargs):
        """
            批量删除任务
        """
        pass

    @abstractmethod
    def cleanup_jobs(self, *args, **kwargs):
        """
            清空所有任务
        """
        pass

    @abstractmethod
    def lookup_job(self, *args, **kwargs):
        """
            查看任务
        """
        pass

    @abstractmethod
    def get_due_jobs(self, *args, **kwargs):
        """
            获取执行中的任务
        """
        pass

    @abstractmethod
    def get_next_run_time(self, *args, **kwargs):
        """
            获取下一次运行时间
        """
        pass

    @abstractmethod
    def get_all_jobs(self, *args, **kwargs):
        """
            获取所有任务
        """
        pass
