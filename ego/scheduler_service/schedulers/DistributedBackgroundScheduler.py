from ego.scheduler.schedulers.Scheduler import Scheduler

from ego.scheduler_service.jobstores.SchedulerServiceJobStore import SchedulerServiceJobStore


class DistributedBackgroundScheduler(Scheduler):
    schedulerServiceJobStore = SchedulerServiceJobStore()

    def register(self, request_body):
        return self.schedulerServiceJobStore.register(data=request_body)

    def unregister(self, *args, **kwargs):
        raise NotImplementedError()

    def start(self, *args, **kwargs):
        raise NotImplementedError()

    def shutdown(self, *args, **kwargs):
        raise NotImplementedError()

    def query_job(self, *args, **kwargs):
        raise NotImplementedError()

    def add_job(
        self,
        id,
        name,
        trigger,
        target=None,
        func=None,
        args=[],
        kwargs={},
        misfire_grace_time=-1,
        coalesce=False,
        max_instances=1,
        executor=None,
        replace_existing=False,
        *e_args,
        **e_kwargs
    ):
        raise NotImplementedError()

    def add_jobs(self, job_list):
        return self.schedulerServiceJobStore.add_jobs(data=job_list)

    def remove_job(self, *args, **kwargs):
        raise NotImplementedError()

    def remove_jobs(self, *args, **kwargs):
        raise NotImplementedError()

    def pause_job(self, *args, **kwargs):
        raise NotImplementedError()

    def resume_job(self, *args, **kwargs):
        raise NotImplementedError()

    def modify_job(self, *args, **kwargs):
        raise NotImplementedError()

    def reschedule_job(self, *args, **kwargs):
        raise NotImplementedError()
