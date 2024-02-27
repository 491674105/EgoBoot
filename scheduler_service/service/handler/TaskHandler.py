from scheduler_service.service.timer.TaskTimer import TaskTimer


class TaskHandler:
    taskTimer = TaskTimer()

    def executor(self, name, task_id, task_uri, request_body={}):
        self.taskTimer.start_up_timer(name=name, task_id=task_id, task_uri=task_uri, request_body=request_body)
