from asyncio import run_coroutine_threadsafe
from asyncio import sleep as a_sleep

from datetime import datetime
from logging import Logger

from ego import applicationContext
from ego.flask_core.FlaskApplication import FlaskApplication
from ego.apscheduler_service.constructors.APSchedulerConstructor import APSchedulerConstructor
from nacos_service.register.NacosRegister import NacosRegister
from nacos_service.listener.ServiceSubscribeListener import ServiceSubscribeListener

from ego.common.constant.config import Base, Scheduler

from ego.utils.time.Time import get_datetime, datetime_format
from ego.utils.network import network

log: Logger


class NacosFlaskApplication(FlaskApplication):
    def __init__(
            self,
            import_name, db_inst,
            template_folder=None, static_folder=None, root_path=None
    ):
        super(NacosFlaskApplication, self).__init__(
            import_name, db_inst, template_folder, static_folder, root_path, output_sys_info_flag=False
        )
        self.sys_scheduler = None

    def __call__(self, clazz):
        super(NacosFlaskApplication, self).__call__(clazz)

        global log
        log = applicationContext.log

        run_coroutine_threadsafe(self.lazy_load_nacos(), self.loop)

        return clazz

    async def lazy_load_nacos(self):
        while not hasattr(applicationContext, Scheduler.SCHEDULER_INIT_FLAG) \
                or not getattr(applicationContext, Scheduler.SCHEDULER_INIT_FLAG):
            log.debug("wait for scheduler init......")
            await a_sleep(1)
        while not hasattr(applicationContext, Scheduler.WAIT_SCHEDULER_LOADED) \
                or getattr(applicationContext, Scheduler.WAIT_SCHEDULER_LOADED):
            log.debug("wait for scheduler loading......")
            await a_sleep(1)

        try:
            if getattr(applicationContext, Scheduler.VALID_SCHEDULER_TYPE) != Scheduler.DEFAULT_SCHEDULER_TYPE:
                self.create_inline_sys_scheduler()
            else:
                self.sys_scheduler = getattr(applicationContext, "sys_scheduler")

            # 注册nacos服务
            log.debug("注册NACOS服务 ---> " + datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
            host_get = applicationContext.base_config[
                getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)
            ]["cloud"]["nacos"]["profile"][applicationContext.env]
            if host_get and host_get == "local":
                try:
                    host_info = network.queryhost()
                except Exception as e:
                    log.exception(e)
                    host_info = network.get_host_by_ipa()
            else:
                host_info = host_get
            self.nacos_register(host_info)
            log.debug("注册NACOS服务完成 ---> " + datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

            # 监听被订阅服务的状态用于feign访问
            log.debug("创建NACOS订阅监听 ---> " + datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
            self.nacos_listen()
            log.debug("创建NACOS订阅监听完成 ---> " + datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

            # 输出当前服务信息
            self.output_server_info(host=host_info)
        except Exception as e:
            log.exception(e)

    def create_inline_sys_scheduler(self):
        scheduler_names = [
            {
                "sch_name": "inline_sys_scheduler",
                "timezone": self.base_config[
                    getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)
                ]["timezone"],
                "skip_start_check": True
            }
        ]
        APSchedulerConstructor.create_schedulers(scheduler_names)
        self.sys_scheduler = getattr(applicationContext, "inline_sys_scheduler")

    def nacos_register(self, host_info):
        nacos_register = NacosRegister(
            host_info,
            applicationContext.port,
            applicationContext.base_config[
                getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)
            ]["application"]["name"],
            applicationContext.nacos_client,
            applicationContext.nacos_config
        )
        metadata = self.create_metadata()
        nacos_register.register(metadata=metadata)
        self.sys_scheduler.add_job(
            id='nacos_register_report_beat_schedule',
            name="nacos_register_report_beat_schedule",
            func=nacos_register.report_beat,
            args=(metadata,),
            trigger="interval",
            seconds=nacos_register.reporting_interval,
            replace_existing=True
        )

    @staticmethod
    def create_metadata():
        metadata = {
            "xxf.version": "local",
            "xxf.build.time": datetime_format(get_datetime(), "%Y-%m-%dT%H:%M:%S.%fZ"),
            "xxf.zone.name": "default-normal",
            "preserved.register.source": "SPRING_CLOUD",
        }

        return metadata

    def nacos_listen(self):
        if "routes" in applicationContext.base_config[getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)]["cloud"]:
            refresh_subscribe = None
            if "refresh_subscribe" in applicationContext.base_config[
                    getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)]["cloud"]:
                refresh_subscribe = applicationContext.base_config[
                    getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)
                ]["cloud"]["refresh_subscribe"]
            service_subscribe_listener = ServiceSubscribeListener(
                nacos_client=applicationContext.nacos_client,
                service_list=applicationContext.base_config[
                    getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)
                ]["cloud"]["routes"],
                ttl=refresh_subscribe
            )
            # 自动订阅任务执行前，优先执行一次订阅，同时加载静态订阅
            service_subscribe_listener.load_static_instance()
            service_subscribe_listener.apply_instance_info()
            self.sys_scheduler.add_job(
                id='nacos_listen_service_subscribe_listener_schedule',
                func=service_subscribe_listener.apply_instance_info,
                trigger="interval",
                seconds=service_subscribe_listener.ttl,
                replace_existing=True
            )

    def output_server_info(self, **kwargs):
        global log
        log.info("--------核心组件已启动--------")
        log.info("---------服务应用信息---------")
        protocol = "http"
        root_path = applicationContext.base_config[getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)]['root_path']
        local_url = f"localhost:{applicationContext.port}/{root_path}"
        local_url = local_url.replace("//", "/")
        log.info(f"{protocol}://{local_url}")
        url = None
        if applicationContext.host != "0.0.0.0":
            url = f"{applicationContext.host}:{applicationContext.port}{root_path}"
        if "host" in kwargs:
            url = f"{kwargs['host']}:{applicationContext.port}{root_path}"

        if url:
            url = url.replace('//', '/')
            log.info(
                f"{protocol}://{url}"
            )

        log.info("---------服务应用信息---------")
