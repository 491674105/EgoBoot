from ego.scheduler.service.SchedulerCoreService import SchedulerCoreService


class TaskService:
    def __init__(self):
        self.ncalls = 0

    def __call__(self, clazz):
        self.clazz = clazz
        self.inst = self.clazz()

        scheduler_jobs = SchedulerCoreService.get_scheduler_jobs()
        if scheduler_jobs is None:
            return clazz

        task_loader = SchedulerCoreService.get_task_loader()
        if not task_loader:
            return clazz
        task_loader.load_task_cls(clazz=clazz)
        return clazz
