from ego.logger.service.LoggerCoreService import LoggerCoreService

from scheduler_service.feign.TaskClientFeign import TaskClientFeign

log = LoggerCoreService.get_logger_instance()


class TaskTimer:
    taskClientFeign = TaskClientFeign()

    def start_up_timer(self, name, task_id, task_uri, request_body):
        log.debug(f"{name} says, task[{task_id}] is running...")
        log.debug(f"task_uri --> {task_uri}")
        log.debug(request_body)

        self.taskClientFeign.start_up_task(
            service_name=request_body["service_name"],
            api_path=task_uri
        )
