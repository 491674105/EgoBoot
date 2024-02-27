from datetime import datetime

from ego import applicationContext
from ego.dispatch.controller.TaskServiceDispatcher import TaskService
from ego.dispatch.controller.TaskDispathcher import Task

log = applicationContext.log
scheduler = applicationContext.sys_scheduler.scheduler


@TaskService()
class TestTask:
    @Task("0 20 14 11 7 * 2022")
    def test(self):
        log.debug(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - test_once...")


    @Task("*/5 * * * * * *")
    def test_once(self):
        scheduler.print_jobs()
        log.debug(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - test task...")
