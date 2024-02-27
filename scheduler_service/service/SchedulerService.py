from ego import routeContainer
from ego.logger.service.LoggerCoreService import LoggerCoreService
from ego.response.Result import Result

log = LoggerCoreService.get_logger_instance()


class SchedulerService:
    def register(self, request_body):
        log.debug(request_body)
        if "service_name" not in request_body or request_body["service_name"] in (None, ""):
            return Result.failed(msg="can not find [service_name]")
        service_name = request_body["service_name"]

        if "address" not in request_body or request_body["address"] in (None, ""):
            return Result.failed(msg="can not find [address]")
        address = request_body["address"]

        if "port" not in request_body or request_body["port"] <= 0:
            return Result.failed(msg="can not find [port]")
        port = request_body["port"]

        routeContainer.add_instance(
            service_name=service_name,
            ip=address,
            port=port
        )
        return Result.success()
