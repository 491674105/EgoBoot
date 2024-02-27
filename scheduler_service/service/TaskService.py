from ego.logger.service.LoggerCoreService import LoggerCoreService
from ego.scheduler.service.SchedulerCoreService import SchedulerCoreService
from ego.response.Result import Result
from ego.common.enum.network.ResultCode import ResultCode

from ego.apscheduler_service.jobstores.BatchSQLAlchemyJobStore import BatchSQLAlchemyJobStore

from scheduler_service.service.handler.TaskHandler import TaskHandler
from scheduler_service.dao.TaskMapper import TaskMapper

log = LoggerCoreService.get_logger_instance()


class TaskService:
    taskMapper = TaskMapper()

    def add_job(self, request_body):
        log.debug(request_body)

        t_kwargs = request_body.copy()
        if "task_id" not in request_body or request_body["task_id"] in (None, ""):
            return Result.failed(ResultCode.BAD_REQUEST.value, "未指定任务ID")
        task_id = request_body["task_id"]
        del request_body["task_id"]
        if "task_name" not in request_body or request_body["task_name"] in (None, ""):
            task_name = task_id
        else:
            task_name = request_body["task_name"]
            del request_body["task_name"]

        if "task_uri" not in request_body or request_body["task_uri"] in (None, ""):
            return Result.failed(msg="can not find [task_uri]")
        task_uri = request_body["task_uri"]
        del request_body["task_uri"]

        if "service_name" not in request_body or request_body["service_name"] in (None, ""):
            return Result.failed(msg="can not find [service_name]")
        del request_body["service_name"]

        business_scheduler = SchedulerCoreService.get_scheduler_instance()
        taskHandler = TaskHandler()
        business_scheduler.add_job(
            id=task_id,
            name=task_name,
            func=taskHandler.executor,
            args=["fearon_task", task_id, task_uri],
            kwargs={"request_body": t_kwargs},
            **request_body
        )
        return Result.success()

    def add_job_list(self, request_body):
        log.debug(request_body)
        if not request_body:
            return Result.failed(ResultCode.BAD_REQUEST.value, "任务信息缺失！")

        business_scheduler = SchedulerCoreService.get_scheduler_instance()
        default_job_stores: BatchSQLAlchemyJobStore = business_scheduler.job_stores["default"]
        q_params = {
            "id_lkw": request_body[0]["task_id"].split(".", 1)[0]
        }
        exist_jobs = default_job_stores.query_jobs(q_params)
        log.debug(exist_jobs)
        exist_job_ids = []
        for exist_job in exist_jobs:
            exist_job_ids.append(exist_job["id"])
        log.debug(exist_job_ids)

        for job_req in request_body:
            log.debug(job_req)
            task_id = job_req["task_id"]
            if task_id in exist_job_ids:
                exist_job_ids.remove(task_id)
            job_res = self.add_job(request_body=job_req)
            if not job_res:
                return Result.failed(msg=f"无法为{job_req['service_name']}创建{job_req['task_name']}任务")
            if job_res["code"] != 200:
                return job_res
        if exist_job_ids:
            default_job_stores.remove_jobs(exist_job_ids)
        return Result.success(msg="任务创建完成！")
