from ego.logger.service.LoggerCoreService import LoggerCoreService
from ego.common.enum.network.HttpMethod import HttpMethod
from ego.dispatch.controller.ControllerDispatcher import Controller
from ego.dispatch.request.RestRequestMappingDispatcher import RestRequestMapping
from ego.response.Result import Result

from scheduler_service.service.TaskService import TaskService


log = LoggerCoreService.get_logger_instance()


@Controller("api/task", sys_root=False)
class TaskApi:
    taskService = TaskService()

    @RestRequestMapping("aj", methods=HttpMethod.POST)
    def add_job(self, request_body):
        """
            新建调度任务
        """
        return Result.success(
            data=self.taskService.add_job(request_body)
        )

    @RestRequestMapping("ajl", methods=HttpMethod.POST)
    def add_job_list(self, request_body):
        """
            批量新建调度任务
        """
        return Result.success(
            data=self.taskService.add_job_list(request_body)
        )
