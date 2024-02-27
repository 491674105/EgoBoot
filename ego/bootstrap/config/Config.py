import logging as logger
from typing import Union
from os import environ

from yaml import safe_load

from env import ENV

from ego import applicationContext, routeContainer
from ego.utils.file import File
from ego.utils.shcmd import sysutils

from ego.common.constant.config import Base, Ego

from ego.exception.type.NullPointException import NullPointException


class Config:
    __default_host = "0.0.0.0"
    __ego_config_key = "ego.original"

    def __init__(self, *args, **kwargs):
        self.ncalls = 0

        if "env" in environ:
            self.env = environ["env"]
        else:
            self.env = ENV
        self.log_level = None
        self.base_config = None
        self.ego_config = None
        self.logger_config = None

        if "ego_config_key" in kwargs:
            self.ego_config_key = kwargs["ego_config_key"]
        else:
            self.ego_config_key = self.__ego_config_key

        if "host" in kwargs:
            self.host = kwargs["host"]
        else:
            self.host = self.__default_host

        self.service_list = []

    def __call__(self, clazz):
        self.clazz = clazz

        setattr(applicationContext, Base.BASE_CONFIG_VALID_KEY, Ego.DEFAULT_EGO_CONFIG_KEY)

        self.load_base_config()
        self.set_env()

        # 配置日志全局日志级别
        self.set_log_level()

        self.update_ego_config()

        self.set_env()

        # 缓存静态订阅
        self.cache_static_subscription()

        return clazz

    def load_base_config(self):
        sysutils.print_logo()

        with open(
                File.path_format(
                    f"{File.get_path(base_path=self.clazz.__module__.split('.')[0])}{Base.DEFAULT_CONFIG_FILE}"
                ),
                mode="r",
                encoding=Base.DEFAULT_ENCODING
        ) as file:
            self.base_config = safe_load(file)
            setattr(applicationContext, "base_config", self.base_config)

    def set_env(self):
        setattr(applicationContext, "env", self.env)
        setattr(applicationContext, "log_level", self.log_level)
        setattr(applicationContext, "host", self.host)
        setattr(applicationContext, "port", self.base_config["server"]["port"])

    def update_ego_config(self):
        self.ego_config = self.base_config
        for key in self.ego_config_key.split('.'):
            value = self.ego_config[key]
            self.ego_config = value

        # 向应用容器中存入基础信息备用
        setattr(
            applicationContext,
            "service_name",
            self.base_config[Ego.DEFAULT_EGO_CONFIG_KEY]["application"]["name"]
        )
        setattr(applicationContext, "ego_config", self.ego_config)

    def set_log_level(self):
        if Ego.DEFAULT_EGO_CONFIG_KEY in self.base_config:
            self.logger_config = self.base_config[Ego.DEFAULT_EGO_CONFIG_KEY]["logger"]
        elif "logger" in self.base_config:
            self.logger_config = self.base_config["logger"]
        else:
            raise NullPointException("can not create logger instance.")

        self.log_level = logger.getLevelName(self.logger_config["level"].upper())

    def cache_static_subscription(self):
        base_valid_config = self.base_config[getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)]
        if "cloud" not in base_valid_config or not base_valid_config["cloud"]:
            setattr(routeContainer, "service_instances", {})
            return
        bv_cloud_config = base_valid_config["cloud"]

        if "routes" not in bv_cloud_config or not bv_cloud_config["routes"]:
            setattr(routeContainer, "service_instances", {})
            return

        self.service_list = bv_cloud_config["routes"]
        for service in self.service_list:
            service_name = service["name"]

            if "static" not in service:
                continue

            static = service["static"]
            routeContainer.add_instance(
                service_name=service_name,
                ip=static["ip"],
                port=static["port"]
            )

    @staticmethod
    def get_config(config_: dict, key_: Union[str, dict]):
        if not config_:
            return None

        if isinstance(key_, str):
            real_key = key_
            default_ = None
            require_ = True
        else:
            real_key = key_["key"]
            default_ = key_["default"]
            require_ = key_["require"]

        if real_key not in config_:
            if require_:
                return None
            return default_
        return config_[real_key]
