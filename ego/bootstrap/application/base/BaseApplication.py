import sys

from typing import Union
from logging import Logger
from os import environ

from time import sleep

from gevent.pywsgi import WSGIServer

from ego import applicationContext
from ego.logger.service.LoggerCoreService import LoggerCoreService
from ego.bootstrap.application.Application import Application
from ego.shutdown.gracefully.GracefullyShutdown import GracefullyShutdown

from ego.common.constant.config import Base
from ego.common.enum.system.SysEnv import SysEnv


class BaseApplication(Application):
    def __init__(self):
        self.server = None
        self.hosting = False
        super().__init__()

        self.log: Union[Logger, None] = None

    def create_server(self):
        # 创建服务器实例
        self.server = WSGIServer(
            (applicationContext.host, applicationContext.port),
            applicationContext.app
        )

    def run(self):
        if not self.log:
            self.log = LoggerCoreService.get_logger_instance()

        # 为当前服务器实例注册停服事件
        self.__register_shutdown_event()

        while not applicationContext.check_blueprint_finish():
            self.log.debug("wait for bp register......")
            sleep(1)

        blueprint_set = applicationContext.get_blueprint_set()
        # self.log.debug(blueprint_set)
        for bp_type in blueprint_set:
            if not blueprint_set[bp_type]:
                continue
            for bp in blueprint_set[bp_type]:
                applicationContext.app.register_blueprint(blueprint=bp)
        self.log.debug("bp register finished.")
        # 写入应用启动标记，此标记仅用于参考框架核心模组（不包含懒加载模组）是否加载完成
        setattr(applicationContext, Base.DEFAULT_APP_LAUNCHED_KEY, True)
        if Base.DEFAULT_HOSTING_KEY in environ and environ[Base.DEFAULT_HOSTING_KEY] == SysEnv.HOSTING_OPEN.value:
            return applicationContext.app

        return None

    @staticmethod
    def __register_shutdown_event():
        gracefully_shutdown = GracefullyShutdown()
        gracefully_shutdown.register()
        sys.excepthook = gracefully_shutdown.exception_handler
