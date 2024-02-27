from sqlalchemy import Column
from sqlalchemy import Integer, BigInteger, SmallInteger, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsProcessPublishInfoDO(Base, BaseEntity):
    __tablename__ = "ops_process_publish_info"

    info_id = Column(BigInteger, primary_key=True, autoincrement=True)
    process_id = Column(BigInteger)
    process_no = Column(String(64))
    sys_priority = Column(Integer)
    env = Column(String(16))
    system_id = Column(BigInteger)
    business_system = Column(String)
    publish_time = Column(BigInteger)
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
