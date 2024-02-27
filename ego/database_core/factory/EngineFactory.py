from sqlalchemy.engine.base import Engine

from ego import applicationContext
from ego.bootstrap.config.Config import Config

from ego.common.constant.config import Base
from ego.common.constant.config import Sqlalchemy


class EngineFactory:
    @staticmethod
    def init_engine(app, db_inst, log=None):
        with app.app_context():
            default_engine: Engine = db_inst.get_engine()
            default_engine.logger.logger = log
            setattr(applicationContext, "engine", default_engine)

            binds = Config.get_config(
                applicationContext.base_config[
                    getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)
                ][Base.ORIGINAL_KEY],
                Sqlalchemy.SQLALCHEMY_BINDS
            )
            if not binds:
                return

            for bind in binds:
                bind_engine: Engine = db_inst.get_engine(bind=bind)
                bind_engine.logger.logger = log
                setattr(applicationContext, f"{bind}_engine", bind_engine)
