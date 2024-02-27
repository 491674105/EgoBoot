from ego import applicationContext
from ego.exception.type.NullPointException import NullPointException

from ego.scheduler.schedulers.Scheduler import Scheduler
from ego.scheduler.loader.TaskLoader import TaskLoader


class SchedulerCoreService:

    @staticmethod
    def get_scheduler_instance(key=None) -> Scheduler:
        if not applicationContext:
            raise NullPointException("ApplicationContext is empty.")

        if key in (None, ""):
            scheduler_name = "business_scheduler"
        else:
            scheduler_name = key

        if not hasattr(applicationContext, scheduler_name):
            return None

        return getattr(applicationContext, scheduler_name)

    @staticmethod
    def get_task_loader() -> TaskLoader:
        if not applicationContext:
            raise NullPointException("ApplicationContext is empty.")
        if not hasattr(applicationContext, "scheduler_taskloader"):
            return None
        return getattr(applicationContext, "scheduler_taskloader")

    @staticmethod
    def get_scheduler_jobs():
        if not applicationContext:
            raise NullPointException("ApplicationContext is empty.")
        if not hasattr(applicationContext, "scheduler_jobs"):
            return {}
        return getattr(applicationContext, "scheduler_jobs")
