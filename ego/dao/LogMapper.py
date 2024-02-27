from sqlalchemy import insert

from ego.database_core.service.DatabaseCoreService import DatabaseCoreService
from ego.dao.BaseMapper import BaseMapper

from ego.common.constant.config import Base

from ego.entity.do.log.OperateLogDO import OperateLogDO
from ego.entity.do.log.OperateLogDetailDO import OperateLogDetailDO


class LogMapper(BaseMapper):
    def __init__(self):
        super().__init__(engine=DatabaseCoreService.get_engine_instance(Base.ENGINE_KEY))

    def insert_operate_log(self, op_log):
        insert_sql = insert(OperateLogDO).values(op_log)
        return self.transactional(sql_struct=insert_sql, get_insert_pk=True)

    def insert_operate_log_detail(self, op_log_detail):
        insert_sql = insert(OperateLogDetailDO).values(op_log_detail)
        return self.transactional(sql_struct=insert_sql, get_insert_pk=True)
