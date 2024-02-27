from ego import applicationContext, routeContainer
from ego.logger.service.LoggerCoreService import LoggerCoreService
from ego.scheduler.service.SchedulerCoreService import SchedulerCoreService

from ego.dispatch.controller.ControllerDispatcher import Controller
from ego.dispatch.request.RestRequestMappingDispatcher import RestRequestMapping
from ego.common.enum.network.HttpMethod import HttpMethod

from ego.response.Result import Result

log = LoggerCoreService.get_logger_instance()


@Controller("actuator", sys_root=False)
class ActuatorController:

    @RestRequestMapping("", methods=HttpMethod.GET)
    def actuator(self):
        return Result.success()

    @RestRequestMapping("routes", methods=HttpMethod.GET)
    def routes(self):
        return Result.success(
            data=routeContainer.service_instances
        )

    @RestRequestMapping("health", methods=HttpMethod.GET)
    def health(self):
        return Result.success(
            data={
                "status": "UP"
            }
        )

    @RestRequestMapping("info", methods=HttpMethod.GET)
    def info(self):
        return Result.success(
            data=applicationContext.base_config["info"]
        )

    @RestRequestMapping("env", methods=HttpMethod.GET)
    def env(self):
        return Result.success()

    @RestRequestMapping("jolokia", methods=HttpMethod.GET)
    def jolokia(self):
        return Result.success()

    @RestRequestMapping("threaddump", methods=HttpMethod.GET)
    def thread_dump(self):
        return Result.success()

    @RestRequestMapping("auditevents", methods=HttpMethod.GET)
    def audit_events(self):
        return Result.success()

    @RestRequestMapping("trace", methods=HttpMethod.GET)
    def trace(self):
        return Result.success()

    @RestRequestMapping("mappings", methods=HttpMethod.GET)
    def mappings(self):
        return Result.success()

    @RestRequestMapping("loggers", methods=HttpMethod.GET)
    def loggers(self):
        return Result.success()

    @RestRequestMapping("flyway", methods=HttpMethod.GET)
    def flyway(self):
        return Result.success()

    @RestRequestMapping("logfile", methods=HttpMethod.GET)
    def logfile(self):
        return Result.success()

    @RestRequestMapping("beans", methods=HttpMethod.GET)
    def beans(self):
        return Result.success()

    @RestRequestMapping("dump", methods=HttpMethod.GET)
    def dump(self):
        return Result.success()

    @RestRequestMapping("caches", methods=HttpMethod.GET)
    def caches(self):
        return Result.success()

    @RestRequestMapping("httptrace", methods=HttpMethod.GET)
    def http_trace(self):
        return Result.success()

    @RestRequestMapping("metrics", methods=HttpMethod.GET)
    def metrics(self):
        return Result.success()

    @RestRequestMapping("liquibase", methods=HttpMethod.GET)
    def liquibase(self):
        return Result.success()

    @RestRequestMapping("refresh", methods=HttpMethod.GET)
    def refresh(self):
        return Result.success()

    @RestRequestMapping("scheduledtasks", methods=HttpMethod.GET)
    def scheduled_tasks(self):
        return Result.success()

    @RestRequestMapping("configprops", methods=HttpMethod.GET)
    def configprops(self):
        return Result.success()

    @RestRequestMapping("heapdump", methods=HttpMethod.GET)
    def heapdump(self):
        return Result.success()

    @RestRequestMapping("scheduler_jobs", methods=HttpMethod.GET)
    def scheduler_jobs(self):
        scheduler_jobs = SchedulerCoreService.get_scheduler_jobs()
        if not scheduler_jobs:
            return Result.success(
                data={}
            )

        result_set = {}
        for task_cls in scheduler_jobs:
            tasks = scheduler_jobs[task_cls]
            for func_name in tasks:
                task = tasks[func_name]
                result_set[task["task_id"]] = task["cron"]
        return Result.success(
            data=result_set
        )

    @RestRequestMapping("prometheus", methods=[HttpMethod.GET, HttpMethod.POST])
    def prometheus(self):
        return Result.success()
