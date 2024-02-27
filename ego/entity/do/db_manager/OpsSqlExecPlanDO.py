from sqlalchemy import Column
from sqlalchemy import SmallInteger, BigInteger, String, DateTime, Text

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsSqlExecPlanDO(Base, BaseEntity):
    __tablename__ = "ops_sql_exec_plan"

    se_plan_id = Column(BigInteger, primary_key=True, autoincrement=True)
    plan_source = Column(SmallInteger)
    business_key = Column(String(64))
    task_id = Column(BigInteger)
    title = Column(String(128))
    exec_type = Column(SmallInteger)
    exec_time = Column(BigInteger)
    env = Column(SmallInteger)
    instance_id = Column(BigInteger)
    exec_inst = Column(String(128))
    exec_db_id = Column(BigInteger)
    exec_db = Column(String(128))
    exec_sql = Column(Text)
    exec_status = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
