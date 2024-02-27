import logging as logger

from ego import applicationContext
from ego.bootstrap.config.Config import Config

from ego.exception.type.NullPointException import NullPointException

from ego.common.constant.config import Base, Ego, Flask


class FlaskConfig(Config):
    __default_host = "0.0.0.0"
    __flask_config_key = "flask.original"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flask_config = None

        if "flask_config_key" in kwargs:
            self.flask_config_key = kwargs["flask_config_key"]
        else:
            self.flask_config_key = self.__flask_config_key

    def __call__(self, clazz):
        self.clazz = clazz

        setattr(applicationContext, Base.BASE_CONFIG_VALID_KEY, Flask.DEFAULT_FLASK_CONFIG_KEY)

        self.load_base_config()

        # 配置日志全局日志级别
        self.set_log_level()

        if Ego.DEFAULT_EGO_CONFIG_KEY in self.base_config:
            self.update_ego_config()
        self.update_flask_config()

        self.set_env()

        # 缓存静态订阅
        self.cache_static_subscription()

        return clazz

    def update_flask_config(self):
        self.flask_config = self.base_config
        for key in self.flask_config_key.split('.'):
            value = self.flask_config[key]
            self.flask_config = value

        setattr(
            applicationContext,
            "service_name",
            self.base_config[getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)]["application"]["name"]
        )
        setattr(applicationContext, "flask_config", self.flask_config)

    def set_log_level(self):
        if Ego.DEFAULT_EGO_CONFIG_KEY in self.base_config:
            self.logger_config = self.base_config[Ego.DEFAULT_EGO_CONFIG_KEY]["logger"]
        elif Flask.DEFAULT_FLASK_CONFIG_KEY in self.base_config:
            self.logger_config = self.base_config[Flask.DEFAULT_FLASK_CONFIG_KEY]["logger"]
        elif "logger" in self.base_config:
            self.logger_config = self.base_config["logger"]
        else:
            raise NullPointException("can not create logger instance.")

        self.log_level = logger.getLevelName(self.logger_config["level"].upper())
        if self.log_level < logger.INFO:
            self.base_config[getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)]["original"]["DEBUG"] = True
            self.base_config[getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)]["original"]["SQLALCHEMY_ECHO"] = True
