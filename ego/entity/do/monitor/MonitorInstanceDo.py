from sqlalchemy import Column
from sqlalchemy import String, Integer, BigInteger, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class MonitorInstanceDo(Base, BaseEntity):
    __tablename__ = "monitor_instance"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    system_id = Column(BigInteger)
    monitor_id = Column(BigInteger)
    server_id = Column(String(255))
    busi_group = Column(String(255))
    busi_group_id = Column(BigInteger)
    cloud = Column(Integer)
    ident = Column(String(255))
    del_flag = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
