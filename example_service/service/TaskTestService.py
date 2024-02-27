from ego.logger.service.LoggerCoreService import LoggerCoreService
from ego.scheduler.service.SchedulerCoreService import SchedulerCoreService

from ego.common.enum.scheduler.TriggerType import TriggerType

from example_service.task.TestCustomTask import TestCustomTask
from example_service.task.TestCustomTask import test_run_date_static, test_run_date_static_no_args

log = LoggerCoreService.get_logger_instance()
sys_scheduler = SchedulerCoreService.get_scheduler_instance(key="sys_scheduler")
business_scheduler = SchedulerCoreService.get_scheduler_instance()


class TaskTestService:
    testCustomTask = TestCustomTask()

    def test_run_date(self, run_date):
        """
            对象方法调用（含入参）
        """
        arg = [1, 2, 33, 54]
        business_scheduler.add_job(
            func=self.testCustomTask.test_run_date,
            trigger=TriggerType.DATE.value,
            run_date=run_date,
            args=[arg]
        )

    def test_run_date_no_args(self, run_date):
        """
            对象方法调用（不含入参）
        """
        business_scheduler.add_job(
            func=self.testCustomTask.test_run_date_no_args,
            trigger=TriggerType.DATE.value,
            run_date=run_date
        )

    def test_run_date_static(self, run_date):
        """
            静态方法调用（含入参）
        """
        arg = [1, 2, 33, 54]
        business_scheduler.add_job(
            func=test_run_date_static,
            trigger=TriggerType.DATE.value,
            run_date=run_date,
            args=[arg]
        )

    def test_run_date_static_no_args(self, run_date):
        """
            静态方法调用（不含入参）
        """
        business_scheduler.add_job(
            func=test_run_date_static_no_args,
            trigger=TriggerType.DATE.value,
            run_date=run_date
        )
