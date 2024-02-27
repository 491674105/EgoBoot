from functools import wraps

from ego.scheduler.service.SchedulerCoreService import SchedulerCoreService


class Task:
    def __init__(self, crontab):
        """
            注册定时任务
            crontab
                * * * * * * *__ year
                | | | | | |____ week -> 1-7
                | | | | |______ month -> 1-12
                | | | |________ day_of_month 1-31
                | | |__________ hour -> 0-23
                | |____________ minute -> 0-59
                |______________ second -> 0-59
        """

        self.ncalls = 0

        self.crontab = crontab

    def __call__(self, func):
        task_loader = SchedulerCoreService.get_task_loader()
        if task_loader:
            task_loader.load_task_func(func=func, crontab=self.crontab)

        @wraps(func)
        def wrapper(*args, **kwargs):
            self.ncalls += 1
            return func(*args, **kwargs)

        return wrapper
