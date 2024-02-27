from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from ego.scheduler.schedulers.Scheduler import Scheduler
from ego.apscheduler_service.jobstores.BatchSQLAlchemyJobStore import BatchSQLAlchemyJobStore
from ego.dao.BaseMapper import BaseMapper


class SingleBackgroundScheduler(Scheduler, BaseMapper):
    def __init__(self, engine, timezone=None):
        super().__init__(engine=engine)

        if timezone:
            self.timezone = timezone
        else:
            self.timezone = utc

        self.scheduler = None
        self.job_stores = {}
        self.executors = {}
        self.job_configs = {}

    def set_job_stores(self, stores):
        for store_key in stores:
            self.job_stores[store_key] = stores[store_key]

    def set_executors(self, executors):
        for executor_key in executors:
            self.executors[executor_key] = executors[executor_key]

    def set_job_configs(self, configs):
        for ck in configs:
            self.job_configs[ck] = configs[ck]

    def create_scheduler_instance(self):
        self.scheduler = BackgroundScheduler(
            jobstores=self.job_stores,
            executors=self.executors,
            job_defaults=self.job_configs,
            timezone=self.timezone
        )

    def register(self, *args, **kwargs):
        raise NotImplementedError()

    def unregister(self, *args, **kwargs):
        raise NotImplementedError()

    def start(self, *args, **kwargs):
        self.scheduler.start(*args, **kwargs)

    def shutdown(self, *args, **kwargs):
        self.scheduler.shutdown(*args, **kwargs)

    def query_job(self, job_id=None, job_name=None, all_job=False):
        """
            查询任务
            job_id: 作业的唯一ID
            job_name: 作业的名字
            all_job: 是否查询所有作业，默认False。该参数生效时，其他参数无效
        """
        jobs = self.to_list(self.scheduler.get_jobs())
        if all_job:
            return jobs

        res_job = []
        for job in jobs:
            if job["id"] == job_id:
                return [job]
            if job["name"] == job_name:
                res_job.append(job)
        return res_job

    def add_job(self, *args, **kwargs):
        self.scheduler.add_job(*args, **kwargs)

    def add_jobs(self, *args, **kwargs):
        raise NotImplementedError()

    def remove_job(self, job_id):
        self.scheduler.remove_job(job_id)

    def remove_jobs(self, *args, **kwargs):
        raise NotImplementedError()

    def pause_job(self, job_id):
        self.scheduler.pause_job(job_id)

    def resume_job(self, job_id):
        self.scheduler.resume_job(job_id)

    def modify_job(self, job_id, **kwargs):
        """
            修改任务信息
            job_id不可修改
        """
        self.query_job(job_id=job_id).modify(**kwargs)

    def reschedule_job(self, job_id, **kwargs):
        self.scheduler.reschedule_job(job_id, **kwargs)

    @staticmethod
    def create_scheduler_with_database(engine, timezone, table_name, coalesce=False, max_instances=3):
        scheduler_ = SingleBackgroundScheduler(engine=engine, timezone=timezone)

        if table_name:
            scheduler_.set_job_stores({
                "default": BatchSQLAlchemyJobStore(engine=engine, tablename=table_name)
            })
        scheduler_.set_executors({
            "default": ThreadPoolExecutor(20),
            "processpool": ProcessPoolExecutor(5)
        })
        scheduler_.set_job_configs({
            "coalesce": coalesce,
            "max_instances": max_instances
        })
        scheduler_.create_scheduler_instance()

        return scheduler_
