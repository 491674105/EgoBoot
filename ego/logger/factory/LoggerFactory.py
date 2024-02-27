from platform import system
from os import environ

from sys import stdout
from os import path, makedirs

from logging import INFO
from logging import getLogger
from logging import StreamHandler, Formatter
from logging.handlers import TimedRotatingFileHandler

from flask import Flask

from ego import applicationContext

from ego.logger.filter.RecordFilter import RecordFilter

from ego.common.constant.config import Base
from ego.common.enum.system.SysEnv import SysEnv


class LoggerFactory:
    __loggers = []

    def __init__(self, app, level=INFO, handlers=None, formatter=None, filters=None):
        self.app = app
        self.level = level

        # 移除默认日志处理器
        getLogger().handlers.clear()

        self.handlers = []
        if handlers:
            self.handlers = handlers

        self.formatter = ""
        if formatter and formatter != "":
            self.formatter = formatter

        self.filters = []
        if filters:
            self.filters = filters

        app.logger.debug(f"logger_level -> {self.level}")

    def init_loggers(self, name=None):
        if not name:
            return
        logger = getLogger(name)
        logger.handlers = self.handlers
        logger.filters = self.filters

    @staticmethod
    def create_log_file(app, logger_config, handlers):
        if Base.DEFAULT_OUTPUT_PATH_KEY not in logger_config:
            return
        if logger_config[Base.DEFAULT_OUTPUT_PATH_KEY] in (None, ""):
            return
        if environ[Base.DEFAULT_RUNNING_MODE_KEY] == SysEnv.RUNNING_MODE_DEVELOPER.value:
            return

        logger_file = logger_config[Base.DEFAULT_OUTPUT_PATH_KEY]
        if Base.DEFAULT_LOGGER_FILE_SUFFIX not in logger_file:
            logger_file = f"{logger_file}{Base.DEFAULT_LOGGER_FILE_SUFFIX}"

        try:
            if logger_file.find("/") == -1:
                log_file_path = f"{getattr(applicationContext, Base.MODULE_PATH_KEY)}{Base.DEFAULT_LOGGER_PATH}/"
                if not path.exists(log_file_path):
                    makedirs(log_file_path)
                logger_file = f"{log_file_path}{logger_file}"
            else:
                logger_path = logger_file.rsplit("/", 1)[0]
                if not path.exists(logger_path):
                    makedirs(logger_path)
        except IOError:
            app.logger.error(f"unable to create the [{logger_file}]")

        file_handler = TimedRotatingFileHandler(
            filename=logger_file,
            interval=1,
            when="D",
            backupCount=0,
            encoding=logger_config["encoding"]
        )
        file_handler.setLevel(applicationContext.log_level)
        handlers.append(file_handler)

    def set_handler(self, handlers: list, formatter: Formatter):
        if handlers:
            self.handlers = handlers

        for h in handlers:
            h.setLevel(self.app.logger.level)
            h.setFormatter(formatter)

    def set_filter(self, filters):
        if filters:
            self.filters = filters

    @staticmethod
    def create_logger(logger_config: dict, app: Flask):
        fmt = Formatter(
            fmt=logger_config["fmt"],
            datefmt=logger_config["datefmt"]
        )
        stream_handler = StreamHandler(stdout)
        stream_handler.setLevel(applicationContext.log_level)
        handlers = [stream_handler]

        if system().lower() != "windows":
            root_paths = getattr(applicationContext, Base.MODULE_PATH_KEY).split("/")
        else:
            root_paths = getattr(applicationContext, Base.MODULE_PATH_KEY).split("\\")

        if not root_paths[-1] or root_paths[-1] == "":
            root_path = root_paths[-3]
        else:
            root_path = root_paths[-2]
        record_filter = RecordFilter(root_path=root_path, service_port=applicationContext.port)

        LoggerFactory.create_log_file(app=app, logger_config=logger_config, handlers=handlers)
        app.logger.level = applicationContext.log_level
        logger_factory = LoggerFactory(
            app=app,
            level=applicationContext.log_level
        )
        logger_factory.set_handler(handlers, fmt)
        logger_factory.set_filter([record_filter])
        logger_factory.init_loggers(app.logger.name)

        return app.logger
