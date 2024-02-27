from ego.dao.BaseMapper import BaseMapper

from ego.common.constant.config import Base

from ego.logger.service.LoggerCoreService import LoggerCoreService
from ego.database_core.service.DatabaseCoreService import DatabaseCoreService

log = LoggerCoreService.get_logger_instance()


class TaskMapper(BaseMapper):

    def __init__(self):
        super().__init__(engine=DatabaseCoreService.get_engine_instance(Base.ENGINE_KEY))
