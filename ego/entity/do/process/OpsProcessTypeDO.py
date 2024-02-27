from sqlalchemy import Column
from sqlalchemy import SmallInteger, BigInteger, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsProcessTypeDO(Base, BaseEntity):
    __tablename__ = "ops_process_type"

    type_id = Column(BigInteger, primary_key=True, autoincrement=True)
    type_name = Column(String(64))
    description = Column(String(255))
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
