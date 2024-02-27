from importlib import import_module

from asyncio import run_coroutine_threadsafe
from asyncio import sleep

from flask import Blueprint, request, g
from flask.views import View

from ego import applicationContext
from ego.bootstrap.config.Config import Config
from ego.bootstrap.service.ConfigCoreService import ConfigCoreService
from ego.logger.service.LoggerCoreService import LoggerCoreService
from ego.coroutine.service.LoopCoreService import LoopCoreService
from ego.scheduler.service.SchedulerCoreService import SchedulerCoreService
from ego.scheduler.loader.TaskLoader import TaskLoader

from ego.common.constant.config import Base
from ego.response.Result import Result
from ego.common.enum.network.HttpMethod import HttpMethod
from ego.common.enum.scheduler.TriggerType import TriggerType
from ego.common.constant.config import Scheduler

from ego.utils.file import File
from ego.utils.network import network

scheduler_config = ConfigCoreService.get_base_config(Scheduler.SCHEDULER_CONFIG_KEY)

app = applicationContext.app
log = None


class SchedulerTaskLoader(TaskLoader):

    def __init__(self, base_load_path, import_all=True):
        self.__service_name = None
        self.__address = None
        self.__port = None
        super().__init__(base_load_path, import_all=import_all)
        self.__bp_set = []

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
        if not self.class_names:
            return
        global log
        log = LoggerCoreService.get_logger_instance()

        self__app_config = ConfigCoreService.get_app_config()
        log.debug(f"app_config --> {self__app_config}")
        self__app_info = Config.get_config(self__app_config, Base.APPLICATION_KEY)
        self.__service_name = self__app_info["name"]
        try:
            self.__address = network.queryhost()
        except Exception as e:
            log.exception(e)
            self.__address = network.get_host_by_ipa()
        self.__port = applicationContext.port
        service_instance = {
            "service_name": self.__service_name,
            "address": self.__address,
            "port": self.__port
        }

        business_scheduler = SchedulerCoreService.get_scheduler_instance()
        sys_scheduler = SchedulerCoreService.get_scheduler_instance("inline_sys_scheduler")
        n_job_id = f"{Config.get_config(scheduler_config, Scheduler.SCHEDULER_SERIVCE_NAME)}_register_report_beat"
        sys_scheduler.add_job(
            id=n_job_id,
            name=n_job_id,
            func=business_scheduler.register,
            kwargs={"request_body": service_instance},
            trigger="interval",
            seconds=Config.get_config(scheduler_config, Scheduler.REPORTING_INTERVAL),
            replace_existing=True
        )

        for class_name in self.class_names:
            import_module(f"{self.base_load_path}.{class_name}")

        applicationContext.save_blueprint(
            bp_type="scheduler_service_bp",
            bp=self.__bp_set
        )
        self.dispatch_tasks()

    def load_task_cls(self, clazz):
        scheduler_jobs = SchedulerCoreService.get_scheduler_jobs()
        if scheduler_jobs is None:
            return

        app_config = ConfigCoreService.get_app_config()
        app_info = Config.get_config(app_config, Base.APPLICATION_KEY)
        service_name = app_info["name"]
        url_prefix = f"/{service_name}"

        def dispatch_request(this, *args, **kwargs):
            if args:
                setattr(g, "args", args)

            if kwargs:
                setattr(g, "kwargs", kwargs)

            run_coroutine_threadsafe(
                SchedulerTaskLoader.request_dispatcher(this),
                LoopCoreService.get_loop_instance()
            )
            return Result.success()

        attrs = {
            "dispatch_request": dispatch_request
        }
        for key in clazz.__dict__:
            if key.find("__") == 0 or key.find(f"_{clazz.__name__}") > 0:
                continue
            attrs[key] = clazz.__dict__[key]

        m_clazz = type(clazz.__name__, (View,), attrs)

        route_ = Blueprint(
            name=clazz.__module__.replace(".", "-"),
            import_name=clazz.__module__,
            url_prefix=url_prefix
        )

        scheduler_records = getattr(applicationContext, "scheduler_records")
        scheduler_record_mappings = {}
        for scheduler_record in scheduler_records[clazz.__module__]:
            api_url = scheduler_record["rule"]
            endpoint = scheduler_record["endpoint"]
            view_func = endpoint.split(".")[-1]
            route_.add_url_rule(
                rule=api_url,
                endpoint=view_func,
                view_func=getattr(m_clazz, "as_view")(view_func),
                methods=scheduler_record["methods"]
            )
            task_uri = f"{url_prefix}/{api_url}"
            scheduler_record_mappings[task_uri] = view_func
            scheduler_jobs[clazz.__name__][view_func]["task_id"] = f"{clazz.__module__}.{view_func}"
            scheduler_jobs[clazz.__name__][view_func]["task_uri"] = task_uri[1:]

        if not hasattr(applicationContext, "scheduler_record_mappings") \
                or not applicationContext.scheduler_record_mappings:
            setattr(applicationContext, "scheduler_record_mappings", scheduler_record_mappings)
        else:
            getattr(applicationContext, "scheduler_record_mappings").update(scheduler_record_mappings)
        # app.register_blueprint(blueprint=route_)
        self.__bp_set.append(route_)

    def load_task_func(self, func, crontab):
        scheduler_jobs = SchedulerCoreService.get_scheduler_jobs()
        if scheduler_jobs is None:
            return

        package_name = func.__module__
        endpoint = f"{package_name}.{func.__name__}"
        api_path = endpoint.replace(".", "/")
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

        scheduler_record = {
            "rule": api_path,
            "endpoint": endpoint,
            "methods": [HttpMethod.GET.value]
        }

        if not hasattr(applicationContext, "scheduler_records"):
            setattr(applicationContext, "scheduler_records", {})

        if package_name in getattr(applicationContext, "scheduler_records"):
            applicationContext.scheduler_records[package_name].append(scheduler_record)
        else:
            applicationContext.scheduler_records[package_name] = [scheduler_record]

    def dispatch_tasks(self):
        global log
        if not log:
            log = LoggerCoreService.get_logger_instance()
        log.debug("dispatch_tasks ---> start")
        scheduler_jobs = SchedulerCoreService.get_scheduler_jobs()

        job_list = []
        for task_dict_key in scheduler_jobs:
            task_dict = scheduler_jobs[task_dict_key]
            for task_func_name in task_dict:
                job_req = {}
                task_info = task_dict[task_func_name]
                log.debug(f"{task_dict_key}:{task_func_name} --> {task_info}")
                job_req["service_name"] = self.__service_name
                job_req["task_id"] = f"{self.__service_name}.{task_info['task_id']}"
                job_req["task_uri"] = task_info["task_uri"]

                job_req["trigger"] = TriggerType.CRON.value
                crontab = task_info["cron"].split()
                job_req["year"] = crontab[6]
                job_req["week"] = crontab[5]
                job_req["month"] = crontab[4]
                job_req["day_of_week"] = crontab[3]
                job_req["hour"] = crontab[2]
                job_req["minute"] = crontab[1]
                job_req["second"] = crontab[0]
                job_list.append(job_req)
        log.debug(job_list)
        business_scheduler = SchedulerCoreService.get_scheduler_instance()
        business_scheduler.add_jobs(job_list=job_list)

    @staticmethod
    async def request_dispatcher(this):
        await sleep(0.001)
        getattr(this, getattr(applicationContext, "scheduler_record_mappings")[request.url_rule.rule])()
