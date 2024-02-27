from typing import Union
from asyncio import sleep as a_sleep

from sys import modules
from importlib import import_module

from ego import applicationContext
from ego.bootstrap.config.Config import Config
from ego.logger.service.LoggerCoreService import LoggerCoreService

from ego.exception.type.NullPointException import NullPointException

from ego.common.constant.config import Base, Scheduler, Network
from ego.common.enum.scheduler.SchedulerType import SchedulerType

from ego.scheduler.constructors.Constructor import Constructor
from ego.scheduler.loader.TaskLoader import TaskLoader

from ego.utils.file import File

log = None


class SchedulerFactory:
    def __init__(self, base_config, *args, **kwargs):
        self.__base_config = base_config
        self.__scheduler_config = None
        self.__sch_type_enum: Union[SchedulerType, None] = None
        self.__scheduler_class = None
        self.__scheduler_package = None
        self.__taskloader_package = None

    @property
    def scheduler_package(self):
        return self.__scheduler_package

    @scheduler_package.setter
    def scheduler_package(self, scheduler_package_):
        self.__scheduler_package = scheduler_package_

    @property
    def taskloader_package(self):
        return self.__taskloader_package

    @taskloader_package.setter
    def taskloader_package(self, taskloader_package_):
        self.__taskloader_package = taskloader_package_

    @property
    def scheduler_class(self):
        return self.__scheduler_class

    @scheduler_class.setter
    def scheduler_class(self, scheduler_class_):
        self.__scheduler_class = scheduler_class_

    def set_env(self):
        setattr(applicationContext, Scheduler.VALID_SCHEDULER_TYPE, Scheduler.DEFAULT_SCHEDULER_TYPE)
        if Scheduler.SCHEDULER_CONFIG_KEY not in self.__base_config:
            self.__scheduler_class = Scheduler.DEFAULT_INLINE_SCHEDULER_CLASS
            self.__scheduler_package = Scheduler.DEFAULT_INLINE_SCHEDULER_PACKAGE
            self.__taskloader_package = Scheduler.DEFAULT_INLINE_TASKLOADER_PACKAGE
            return

        self.__scheduler_config = self.__base_config[Scheduler.SCHEDULER_CONFIG_KEY]
        scheduler_type = Config.get_config(self.__scheduler_config, Scheduler.SCHEDULER_TYPE)
        setattr(applicationContext, Scheduler.VALID_SCHEDULER_TYPE, scheduler_type)
        self.__scheduler_class = Config.get_config(self.__scheduler_config, Scheduler.SCHEDULER_CLASS)
        if self.__scheduler_class in (None, ""):
            self.__scheduler_class = Scheduler.DEFAULT_INLINE_SCHEDULER_CLASS

        self.__scheduler_package = Config.get_config(self.__scheduler_config, Scheduler.SCHEDULER_PACKAGE)
        if self.__scheduler_package in (None, ""):
            if self.__scheduler_class not in Scheduler.SCHEDULER_WORKER_CLASS:
                raise NullPointException("unknown scheduler worker class.")
            self.__scheduler_package = Scheduler.SCHEDULER_WORKER_CLASS[self.__scheduler_class]

        self.__taskloader_package = Config.get_config(self.__scheduler_config, Scheduler.SCHEDULER_TASK_LOADER)
        if self.__taskloader_package in (None, ""):
            raise NullPointException("unknown scheduler taskloader class.")

    @staticmethod
    def create_template(location, *args, **kwargs) -> Constructor:
        class_name = location.rsplit(".", 1)[1]
        if location not in modules:
            this_module = import_module(location)
            return getattr(this_module, class_name)(*args, **kwargs)

        this_module = modules[location]
        return getattr(this_module, class_name)(*args, **kwargs)

    @classmethod
    async def init_schedulers(cls, base_config, *args, **kwargs):
        global log
        log = LoggerCoreService.get_logger_instance()

        while not hasattr(applicationContext, Base.DEFAULT_CORE_LOADED_KEY) \
                or not getattr(applicationContext, Base.DEFAULT_CORE_LOADED_KEY):
            log.debug("等待核心模块加载完成......")
            await a_sleep(1)
        setattr(applicationContext, Scheduler.SCHEDULER_INIT_FLAG, True)

        setattr(applicationContext, "scheduler_jobs", {})
        try:
            factory = cls(base_config, *args, **kwargs)
            factory.set_env()

            scheduler_type = getattr(applicationContext, Scheduler.VALID_SCHEDULER_TYPE)
            log.debug(f"scheduler_type --> {scheduler_type}")
            if scheduler_type == Scheduler.DEFAULT_SCHEDULER_TYPE:
                setattr(applicationContext, Scheduler.WAIT_SCHEDULER_LOADED, True)
            else:
                setattr(applicationContext, Scheduler.WAIT_SCHEDULER_LOADED, False)
                while not hasattr(applicationContext, Network.SUBSCRIBE_FLAG) \
                        or not getattr(applicationContext, Network.SUBSCRIBE_FLAG):
                    log.debug("等待微服务订阅完成......")
                    await a_sleep(1)

            constructor = SchedulerFactory.create_template(location=factory.scheduler_package)
            constructor.constructor(base_config=base_config)

            if not hasattr(applicationContext, Base.MODULE_PATH_KEY) \
                    or getattr(applicationContext, Base.MODULE_PATH_KEY) is None:
                raise NullPointException("unknown module path.")

            module_path = getattr(applicationContext, Base.MODULE_PATH_KEY)
            mp_list = module_path.split(File.get_sys_path_delimiter())
            if len(mp_list) > 1:
                if mp_list[-1] in (None, ""):
                    base_path = mp_list[-2]
                else:
                    base_path = mp_list[-1]
            else:
                base_path = mp_list[0]

            if base_path in (None, ""):
                base_path = "task"
            else:
                base_path = f"{base_path}.task"

            class_name = factory.taskloader_package.rsplit(".", 1)[1]
            this_module = import_module(factory.taskloader_package)
            loader_class = getattr(this_module, class_name)
            loader: TaskLoader = loader_class(base_load_path=base_path)
            setattr(applicationContext, "scheduler_taskloader", loader)
            loader.load_tasks()

            setattr(applicationContext, Scheduler.WAIT_SCHEDULER_LOADED, False)
            applicationContext.mark_blueprint(bp_type="scheduler_service_bp", delete=True)
            return factory
        except ModuleNotFoundError as e:
            log.warning(e)
            setattr(applicationContext, Scheduler.WAIT_SCHEDULER_LOADED, False)
            applicationContext.mark_blueprint(bp_type="scheduler_service_bp", delete=True)
            return None
        except Exception as e:
            log.exception(e)
            setattr(applicationContext, Scheduler.WAIT_SCHEDULER_LOADED, True)
            applicationContext.mark_blueprint(bp_type="scheduler_service_bp", delete=True)
            return None
