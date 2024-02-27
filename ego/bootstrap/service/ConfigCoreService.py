
from ego import applicationContext
from ego.exception.type.NullPointException import NullPointException

from ego.common.constant.config import Base


class ConfigCoreService:

    @staticmethod
    def get_base_config(key=None):
        if not applicationContext:
            raise NullPointException("ApplicationContext is empty.")

        if not key or key == "":
            return applicationContext.base_config

        if key not in applicationContext.base_config:
            raise NullPointException(f"Unable to find information related to [{key}].")
        return applicationContext.base_config[key]

    @staticmethod
    def get_app_config(key=None):
        if not applicationContext:
            raise NullPointException("ApplicationContext is empty.")

        app_config = ConfigCoreService.get_base_config(getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY))
        if not key or key == "":
            return app_config

        if key not in app_config:
            raise NullPointException(f"Unable to find information related to [{key}].")
        return app_config[key]
