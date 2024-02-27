from ego.common.enum.network.HttpMethod import HttpMethod

from ego.bootstrap.config.Config import Config
from ego.bootstrap.service.ConfigCoreService import ConfigCoreService
from ego.logger.service.LoggerCoreService import LoggerCoreService
from ego.dispatch.feign.FeignMappingDispatch import FeignMapping

from ego.common.constant.config import Scheduler

from ego.scheduler.jobstores.JobStore import JobStore

log = LoggerCoreService.get_logger_instance()
scheduler_config = ConfigCoreService.get_base_config(Scheduler.SCHEDULER_CONFIG_KEY)


class SchedulerServiceJobStore(JobStore):
    @FeignMapping(
        service_name=Config.get_config(scheduler_config, Scheduler.SCHEDULER_SERIVCE_NAME),
        uri="/api/scheduler/register",
        method=HttpMethod.POST,
        timeout=8
    )
    def register(self, params=None, data=None, response=None):
        if not response:
            log.error("服务器未响应！")
            return False

        if response["code"] != 200:
            log.error(response)
            return False

        return True

    @FeignMapping(
        service_name=Config.get_config(scheduler_config, Scheduler.SCHEDULER_SERIVCE_NAME),
        uri="/api/task/aj",
        method=HttpMethod.POST,
        timeout=8
    )
    def add_job(self, params=None, data=None, response=None):
        if not response:
            log.error("服务器未响应！")
            return False

        if response["code"] != 200:
            log.error(response)
            return False

        return True

    @FeignMapping(
        service_name=Config.get_config(scheduler_config, Scheduler.SCHEDULER_SERIVCE_NAME),
        uri="/api/task/ajl",
        method=HttpMethod.POST,
        timeout=8
    )
    def add_jobs(self, params=None, data=None, response=None):
        if not response:
            log.error("服务器未响应！")
            return False

        if response["code"] != 200:
            log.error(response)
            return False

        return True

    def update_job(self, *args, **kwargs):
        """
            更新任务
        """
        raise NotImplementedError()

    def update_jobs(self, *args, **kwargs):
        """
            批量更新任务
        """
        raise NotImplementedError()

    def remove_job(self, *args, **kwargs):
        """
            删除任务
        """
        raise NotImplementedError()

    def remove_jobs(self, *args, **kwargs):
        """
            批量删除任务
        """
        raise NotImplementedError()

    def cleanup_jobs(self, *args, **kwargs):
        """
            清空所有任务
        """
        raise NotImplementedError()

    def lookup_job(self, *args, **kwargs):
        """
            查看任务
        """
        raise NotImplementedError()

    def get_due_jobs(self, *args, **kwargs):
        """
            获取执行中的任务
        """
        raise NotImplementedError()

    def get_next_run_time(self, *args, **kwargs):
        """
            获取下一次运行时间
        """
        raise NotImplementedError()

    def get_all_jobs(self, *args, **kwargs):
        """
            获取所有任务
        """
        raise NotImplementedError()
