from sqlalchemy import Column
from sqlalchemy import SmallInteger, BigInteger, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsConfigUpdatePlanDO(Base, BaseEntity):
    __tablename__ = "ops_config_update_plan"

    cu_plan_id = Column(BigInteger, primary_key=True, autoincrement=True)
    plan_source = Column(SmallInteger)
    business_key = Column(String(64))
    task_id = Column(BigInteger)
    cid = Column(BigInteger)
    config_file = Column(String(128))
    cache_conf = Column(String(128))
    update_status = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
