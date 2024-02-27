from ego import applicationContext
from ego.scheduler.constructors.Constructor import Constructor

from ego.scheduler_service.schedulers.DistributedBackgroundScheduler import DistributedBackgroundScheduler


class SchedulerServiceConstructor(Constructor):
    @staticmethod
    def constructor(base_config, *args, **kwargs):
        scheduler = DistributedBackgroundScheduler()
        setattr(applicationContext, "business_scheduler", scheduler)
