from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, BigInteger, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class ServiceBackendInstanceDO(Base, BaseEntity):
    __tablename__ = "registe_service_jar_detail"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    service_id = Column(BigInteger, ForeignKey("service_info.service_id"))
    service_name = Column(String(255))
    healthy_instance = Column(String(255))
    port = Column(Integer)
    env = Column(String(255))
    heap_memory = Column(Integer)
    xxf_zone = Column(String(255))
    status = Column(Integer)
    del_flag = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    profile_active = Column(String(255))
