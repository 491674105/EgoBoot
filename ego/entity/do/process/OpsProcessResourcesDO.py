from sqlalchemy import Column
from sqlalchemy import SmallInteger, BigInteger, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsProcessResourcesDO(Base, BaseEntity):
    __tablename__ = "ops_process_resources"

    resource_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(64))
    process_type = Column(SmallInteger)
    description = Column(String(64))
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
