from importlib import import_module
from time import sleep
from asyncio import run_coroutine_threadsafe
from asyncio import sleep as a_sleep

from logging import Logger

from flask import Flask

from ego import applicationContext, routeContainer
from ego.bootstrap.application.Application import Application

from ego.common.constant.config import Base, Json, Network, Scheduler

from ego.logger.factory.LoggerFactory import LoggerFactory
from ego.database_core.factory.EngineFactory import EngineFactory
from ego.scheduler.factory.SchedulerFactory import SchedulerFactory
from ego.filter.FilterFactory import FilterFactory
from ego.interceptor.InterceptorFactory import InterceptorFactory
from ego.listener.ListenerFactory import ListenerFactory

from ego.coroutine.asynchronous.AsyncCoroutine import AsyncCoroutine

from ego.exception.type.NullPointException import NullPointException

from ego.utils.file.File import get_path

log: Logger


class FlaskApplication(Application):
    def __init__(
            self,
            import_name, db_inst,
            template_folder=None, static_folder=None, root_path=None,
            *args, **kwargs
    ):
        super().__init__()

        if "output_sys_info_flag" in kwargs:
            self.__output_sys_info_flag = kwargs["output_sys_info_flag"]
        else:
            self.__output_sys_info_flag = True
        self.app = Flask(
            import_name,

            template_folder=template_folder,
            static_folder=static_folder,
            root_path=root_path,
        )
        self.db_inst = db_inst
        self.logger_config = None

    def __call__(self, clazz):
        self.clazz = clazz
        setattr(applicationContext, Base.DEFAULT_CORE_LOADED_KEY, False)
        setattr(applicationContext, Base.DEFAULT_APP_LAUNCHED_KEY, False)
        setattr(applicationContext, Scheduler.SCHEDULER_INIT_FLAG, False)
        setattr(applicationContext, Scheduler.WAIT_SCHEDULER_LOADED, True)
        setattr(applicationContext, Network.SUBSCRIBE_FLAG, False)
        setattr(applicationContext, Base.DEFAULT_LLM_KEY, {})
        setattr(applicationContext, Base.DEFAULT_LML_KEY, {})
        setattr(applicationContext, Base.DEFAULT_BRS_KEY, {})
        setattr(applicationContext, Base.DEFAULT_WBC_KEY, set())

        # 缓存模块服务所在的物理路径
        self.module_path = get_path(self.clazz.__module__.split('.')[0])
        setattr(applicationContext, Base.MODULE_PATH_KEY, self.module_path)

        # 更新flask_app应用配置
        self.flask_config = applicationContext.flask_config
        self.app.config.update(applicationContext.flask_config)
        setattr(applicationContext, "app", self.app)
        self.base_config = applicationContext.base_config
        applicationContext.mark_blueprint(bp_type="default_service_bp")

        # 创建全局日志处理器
        global log
        log = LoggerFactory.create_logger(
            logger_config=applicationContext.base_config[
                getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)
            ]["logger"],
            app=self.app
        )
        setattr(routeContainer, "log", log)
        setattr(applicationContext, "log", log)
        log.debug("---------服务配置项---------")
        for key in self.app.config.keys():
            log.debug(key + " ---> " + str(self.app.config.get(key)))
        log.debug("---------服务配置项---------")

        # 创建异步事件容器
        async_coroutine = AsyncCoroutine()
        async_coroutine.start()
        setattr(applicationContext, "loop_thread", async_coroutine)
        loop_create_timeout = 30
        while True:
            if loop_create_timeout <= 0:
                raise NullPointException("Can't create the loop.")
            if not async_coroutine.loop:
                loop_create_timeout -= 1
                sleep(1)
                continue
            self.loop = async_coroutine.loop
            setattr(applicationContext, "loop", async_coroutine.loop)
            break

        # 创建全局用户session容器
        setattr(applicationContext, "user_sessions", {})
        setattr(applicationContext, "uri_dict", {})
        setattr(applicationContext, "record_log_endpoints", {})

        # 创建全局db对象，用于model操作
        self.db_inst.init_app(self.app)
        setattr(applicationContext, "db", self.db_inst)

        # 创建全局数据库操作引擎
        EngineFactory.init_engine(self.app, self.db_inst, log)

        # 启用调度模块
        run_coroutine_threadsafe(
            SchedulerFactory.init_schedulers(base_config=applicationContext.base_config),
            self.loop
        )
        applicationContext.mark_blueprint(bp_type="scheduler_service_bp")

        # 重载全局json编码方式
        if Json.DEFAULT_JSON_ENCODER_KEY in self.base_config[getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)]:
            try:
                encoder_package = self.base_config[
                    getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)
                ][Json.DEFAULT_JSON_ENCODER_KEY]
                self.app.json = getattr(
                    import_module(encoder_package),
                    encoder_package.rsplit('.', 1)[1]
                )(self.app)
            except Exception as e:
                # 调用默认序列化
                log.error(e)
                self.app.json = getattr(
                    import_module(Json.DEFAULT_JSON_ENCODER_PACKAGE),
                    Json.DEFAULT_JSON_ENCODER_PACKAGE.rsplit('.', 1)[1]
                )(self.app)

        # 初始化过滤器
        FilterFactory.init_filter()

        # 初始化拦截器
        InterceptorFactory.init_interceptor()

        # 初始化监听管理
        ListenerFactory.load_manager()

        # 通知所有等待核心模块加载完成的懒加载组件
        setattr(applicationContext, Base.DEFAULT_CORE_LOADED_KEY, True)

        # 输出当前服务信息
        if self.__output_sys_info_flag:
            run_coroutine_threadsafe(self.output_server_info(), self.loop)
            self.__output_sys_info_flag = False

        run_coroutine_threadsafe(self.launch_lazy_load_modules(), self.loop)

        return clazz

    async def output_server_info(self, **kwargs):
        while not hasattr(applicationContext, Base.DEFAULT_APP_LAUNCHED_KEY) \
                or not getattr(applicationContext, Base.DEFAULT_APP_LAUNCHED_KEY):
            await a_sleep(1)

        global log

        log.info("--------核心组件已启动--------")
        log.info("---------服务应用信息---------")
        setattr(applicationContext, Network.SUBSCRIBE_FLAG, True)
        protocol = "http"
        root_path = applicationContext.base_config[getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)]['root_path']
        log.info(f"{protocol}://localhost:{applicationContext.port}/{root_path}")
        if applicationContext.host != "0.0.0.0":
            log.info(
                f"{protocol}://{applicationContext.host}:{applicationContext.port}/{root_path}"
            )

        log.info("---------服务应用信息---------")

    @staticmethod
    async def launch_lazy_load_modules():
        global log

        log.debug("检查懒加载模组前置启动条件是否满足......")
        while not hasattr(applicationContext, Base.DEFAULT_APP_LAUNCHED_KEY) \
                or not getattr(applicationContext, Base.DEFAULT_APP_LAUNCHED_KEY):
            await a_sleep(1)

        log.debug("检查懒加载模组......")
        if not hasattr(applicationContext, Base.DEFAULT_LLM_KEY):
            log.debug("未配置懒加载。")
            return

        if not getattr(applicationContext, Base.DEFAULT_LLM_KEY):
            log.debug("懒加载组件列表为空。")
            return

        lazy_load_modules = getattr(applicationContext, Base.DEFAULT_LLM_KEY)
        log.debug("准备启动懒加载模组......")

        for l_id in lazy_load_modules:
            log.debug(f"准备启动{l_id}模块。")
            lazy_load_module = lazy_load_modules[l_id]
            lazy_load_module["loader"](*lazy_load_module["args"], **lazy_load_module["kwargs"])

            applicationContext.lazy_module_launched[l_id] = True

        log.debug("懒加载模组启动完成。")

    def create_server(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        pass
