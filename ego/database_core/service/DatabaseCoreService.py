from sqlalchemy.engine.base import Engine
from sqlalchemy import dialects

from ego import applicationContext
from ego.exception.type.NullPointException import NullPointException


class DatabaseCoreService:
    @staticmethod
    def get_engine_instance(key=None) -> Engine:
        if not applicationContext:
            raise NullPointException("ApplicationContext is empty.")

        if not key or key == "":
            inst_name = "engine"
        else:
            inst_name = key

        return getattr(applicationContext, inst_name)

    @staticmethod
    def get_dialect_instance(engine=None, dialect_name=None):
        if engine:
            return getattr(dialects, engine.dialect.name).dialect()

        if dialect_name and dialect_name != "":
            return getattr(dialects, dialect_name).dialect()
