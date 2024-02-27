from logging import Logger

from ego import applicationContext
from ego.exception.type.NullPointException import NullPointException


class LoggerCoreService:

    @staticmethod
    def get_logger_instance(key=None) -> Logger:
        if not applicationContext:
            raise NullPointException("ApplicationContext is empty.")

        if not key or key == "":
            logger_name = "log"
        else:
            logger_name = key

        return getattr(applicationContext, logger_name)
