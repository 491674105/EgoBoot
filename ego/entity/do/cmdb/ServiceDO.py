from sqlalchemy import Column
from sqlalchemy import String, SmallInteger, BigInteger, Text, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class ServiceDO(Base, BaseEntity):
    __tablename__ = "service_info"

    service_id = Column(BigInteger, primary_key=True, autoincrement=True)
    service_name = Column(String(255))
    port = Column(String(255))
    system_id = Column(BigInteger)
    service_type = Column(String(30))
    os_type = Column(String(30))
    build_flag = Column(SmallInteger)
    template = Column(String(128))
    flag = Column(SmallInteger)
    status = Column(SmallInteger)
    publish_flag = Column(SmallInteger)
    mark = Column(Text)
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
