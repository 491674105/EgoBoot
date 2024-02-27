from ego.logger.service.LoggerCoreService import LoggerCoreService
from ego.common.enum.network.HttpMethod import HttpMethod
from ego.dispatch.controller.ControllerDispatcher import Controller
from ego.dispatch.request.RestRequestMappingDispatcher import RestRequestMapping
from ego.response.Result import Result

from scheduler_service.service.SchedulerService import SchedulerService


log = LoggerCoreService.get_logger_instance()


@Controller("api/scheduler", sys_root=False)
class SchedulerApi:
    schedulerService = SchedulerService()

    @RestRequestMapping("register", methods=HttpMethod.POST)
    def register(self, request_body):
        """
            注册
        """
        return Result.success(
            data=self.schedulerService.register(request_body)
        )
