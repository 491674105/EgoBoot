from importlib import import_module

from apscheduler.triggers.date import DateTrigger

from ego.logger.service.LoggerCoreService import LoggerCoreService
from ego.scheduler.service.SchedulerCoreService import SchedulerCoreService
from ego.scheduler.loader.TaskLoader import TaskLoader
from ego.apscheduler_service.triggers.AccurateCronTrigger import AccurateCronTrigger

from ego.utils.file import File


class APSchedulerTaskLoader(TaskLoader):

    def __init__(self, base_load_path, import_all=True):
        super().__init__(base_load_path, import_all=import_all)

    def load_tasks(self):
        self.scanner()
        self.load()

    def scanner(self):
        self.class_names = File.query_file_name_list(
            root_path=self.real_path,
            exclude_folder=self._exclude_folder,
            exclude_name=self._exclude_name,
        )

    def load(self):
        for class_name in self.class_names:
            import_module(f"{self.base_load_path}.{class_name}")

        self.dispatch_tasks()

    def load_task_cls(self, clazz):
        scheduler_jobs = SchedulerCoreService.get_scheduler_jobs()
        if scheduler_jobs is None:
            return

        inst = clazz()
        task_info = scheduler_jobs[clazz.__name__].copy()
        for task_func_name in task_info:
            scheduler_jobs[clazz.__name__][task_func_name]["task_func"] = getattr(inst, task_func_name)
            scheduler_jobs[clazz.__name__][task_func_name]["task_id"] = f"{clazz.__module__}.{task_func_name}"

    def load_task_func(self, func, crontab):
        scheduler_jobs = SchedulerCoreService.get_scheduler_jobs()
        if scheduler_jobs is None:
            return

        names = func.__qualname__.split('.')
        if names[0] in scheduler_jobs:
            scheduler_jobs[names[0]][names[1]] = {
                "cron": crontab
            }
        else:
            scheduler_jobs[names[0]] = {
                names[1]: {
                    "cron": crontab
                }
            }

    @staticmethod
    def dispatch_tasks():
        log = LoggerCoreService.get_logger_instance()
        log.debug("dispatch_tasks ---> start")

        # 获取已有的持久化业务级调度计划
        log.debug("dispatch_tasks ---> running")
        business_scheduler = SchedulerCoreService.get_scheduler_instance()
        business_job_ids = set()
        business_jobs = business_scheduler.query_job(all_job=True)
        log.debug(business_jobs)
        for business_job in business_jobs:
            if not isinstance(business_job["trigger"], DateTrigger):
                business_job_ids.add(business_job["id"])

        scheduler_jobs = SchedulerCoreService.get_scheduler_jobs()
        for task_dict_key in scheduler_jobs:
            task_dict = scheduler_jobs[task_dict_key]
            for task_info_key in task_dict:
                task_info = task_dict[task_info_key]
                business_scheduler.add_job(
                    id=task_info["task_id"],
                    name=task_info["task_id"],
                    func=task_info["task_func"],
                    trigger=AccurateCronTrigger.from_crontab(task_info["cron"]),
                    replace_existing=True
                )
                if task_info["task_id"] in business_job_ids:
                    business_job_ids.remove(task_info["task_id"])
        if business_job_ids:
            for business_job_id in business_job_ids:
                log.debug(f"准备删除无效任务 ---> {business_job_id}")
                business_scheduler.remove_job(job_id=business_job_id)
                log.debug(f"删除完成 ---> {business_job_id}")
        log.debug("__dispatch_tasks ---> end")
