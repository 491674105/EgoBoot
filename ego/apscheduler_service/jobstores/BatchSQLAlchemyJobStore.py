import dill as pickle

from apscheduler.job import Job
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.sqlalchemy import datetime_to_utc_timestamp
from apscheduler.jobstores.sqlalchemy import JobLookupError

from sqlalchemy import delete, update, select
from sqlalchemy.dialects.mysql import Insert
from sqlalchemy import text

from ego.logger.service.LoggerCoreService import LoggerCoreService
from ego.database_core.service.DatabaseCoreService import DatabaseCoreService
from ego.scheduler.jobstores.JobStore import JobStore

from ego.dao.BaseMapper import BaseMapper


class BatchSQLAlchemyJobStore(SQLAlchemyJobStore, JobStore):
    def __init__(self, *args, **kwargs):
        super(BatchSQLAlchemyJobStore, self).__init__(*args, **kwargs)
        self.baseMapper = BaseMapper(engine=kwargs["engine"])

        self.__log = LoggerCoreService.get_logger_instance()

    def add_job(self, job):
        jobs = [{
            'id': job.id,
            'next_run_time': datetime_to_utc_timestamp(job.next_run_time),
            'job_state': pickle.dumps(obj=job.__getstate__(), protocol=self.pickle_protocol)
        }]
        insert_sql = Insert(self.jobs_t).values(jobs)

        kw = {}
        for key in jobs[0].keys():
            kw[key] = text(f"VALUES({key})")
        on_duplicate_key_sql = insert_sql.on_duplicate_key_update(**kw)
        with self.engine.begin() as connection:
            try:
                connection.execute(
                    on_duplicate_key_sql.compile(dialect=DatabaseCoreService.get_dialect_instance(self.engine))
                ).rowcount
            except Exception as e:
                self.__log.warning(e)

    def add_jobs(self, jobs):
        restore_jobs = []
        for job in jobs:
            restore_jobs.append({
                'id': job.id,
                'next_run_time': datetime_to_utc_timestamp(job.next_run_time),
                'job_state': pickle.dumps(obj=job.__getstate__(), protocol=self.pickle_protocol)
            })

        restore_jobs = [{
            'id': job.id,
            'next_run_time': datetime_to_utc_timestamp(job.next_run_time),
            'job_state': pickle.dumps(obj=job.__getstate__(), protocol=self.pickle_protocol)
        }]
        insert_sql = Insert(self.jobs_t).values(restore_jobs)

        kw = {}
        for key in restore_jobs[0].keys():
            kw[key] = text(f"VALUES({key})")
        on_duplicate_key_sql = insert_sql.on_duplicate_key_update(**kw)
        with self.engine.begin() as connection:
            try:
                connection.execute(
                    on_duplicate_key_sql.compile(dialect=DatabaseCoreService.get_dialect_instance(self.engine))
                ).rowcount
            except Exception as e:
                self.__log.warning(e)

    def update_job(self, job):
        update_sql = update(
            self.jobs_t
        ).where(
            self.jobs_t.c.id == job.id
        ).values({
            "next_run_time": datetime_to_utc_timestamp(job.next_run_time),
            "job_state": pickle.dumps(job.__getstate__(), self.pickle_protocol)
        })
        with self.engine.begin() as connection:
            rowcount = connection.execute(
                update_sql.compile(dialect=DatabaseCoreService.get_dialect_instance(self.engine))
            ).rowcount
            if rowcount == 0:
                raise JobLookupError(job.id)

    def update_jobs(self, jobs):
        raise NotImplementedError()

    def remove_job(self, job_id):
        super().remove_job(job_id)

    def remove_jobs(self, job_ids):
        delete_sql = delete(
            self.jobs_t
        ).where(
            self.jobs_t.c.id.in_(job_ids)
        )
        with self.engine.begin() as connection:
            rowcount = connection.execute(
                delete_sql.compile(dialect=DatabaseCoreService.get_dialect_instance(self.engine))
            ).rowcount
            if rowcount == 0:
                self.__log.warning(f"删除定时任务失败！job_id_list --> [{job_ids}]")

    def cleanup_jobs(self):
        super().remove_all_jobs()

    def lookup_job(self, job_id):
        selectable = select([self.jobs_t.c.job_state]).where(self.jobs_t.c.id == job_id)
        job_state = self.engine.execute(selectable).scalar()
        return self._reconstitute_job(job_state) if job_state else None

    def get_due_jobs(self, now):
        return super().get_due_jobs(now)

    def get_next_run_time(self):
        return super().get_next_run_time()

    def get_all_jobs(self):
        return super().get_all_jobs()

    def query_jobs(self, request_body):
        select_sql = select(
            self.jobs_t.c.id,
            self.jobs_t.c.next_run_time
        )

        if "id_lkw" in request_body and request_body["id_lkw"] not in (None, ""):
            select_sql = select_sql.where(
                self.jobs_t.c.id.like(f"{request_body['id_lkw']}%")
            )
        with self.engine.begin() as connect:
            result_set = connect.execute(
                select_sql.compile(dialect=DatabaseCoreService.get_dialect_instance(self.engine))
            ).all()
            if not result_set:
                return []
            else:
                return self.baseMapper.to_list(result_set=result_set, include_none=True)

    def _reconstitute_job(self, job_state):
        job_state = pickle.loads(job_state)
        job_state['jobstore'] = self
        job = Job.__new__(Job)
        job.__setstate__(job_state)
        job._scheduler = self._scheduler
        job._jobstore_alias = self._alias
        return job
