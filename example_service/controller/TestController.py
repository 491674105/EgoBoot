from ego.logger.service.LoggerCoreService import LoggerCoreService
from ego.common.enum.network.HttpMethod import HttpMethod
from ego.dispatch.controller.ControllerDispatcher import Controller
from ego.dispatch.request.RestRequestMappingDispatcher import RestRequestMapping

from example_service.service.TaskTestService import TaskTestService


log = LoggerCoreService.get_logger_instance()


@Controller("register/warrant/test")
class TestController:
    taskTestService = TaskTestService()

    @RestRequestMapping("/v1/test", methods=[HttpMethod.GET, HttpMethod.POST])
    def index(self, request_body=None):
        run_date = "2022-11-11 11:19:20"

        # 对象方法调用（含入参）
        self.taskTestService.test_run_date(run_date)

        # 对象方法调用（不含入参）
        self.taskTestService.test_run_date_no_args(run_date)

        # 静态方法调用（含入参）
        self.taskTestService.test_run_date_static(run_date)

        # 静态方法调用（不含入参）
        self.taskTestService.test_run_date_static_no_args(run_date)

        return request_body
