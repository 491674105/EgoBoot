from sqlalchemy import Column
from sqlalchemy import String, SmallInteger, Integer, BigInteger, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class ServiceInstanceDO(Base, BaseEntity):
    __tablename__ = "service_instance"

    inst_id = Column(BigInteger, primary_key=True, autoincrement=True)
    cloud_id = Column(BigInteger)
    service_id = Column(BigInteger)
    service_name = Column(String(64))
    address = Column(String(128))
    inst_port = Column(Integer)
    heap_memory = Column(Integer)
    inst_env = Column(String(16))
    inst_config_zone = Column(String(32))
    build_cmd = Column(String(1024))
    start_cmd = Column(String(1024))
    cdn_url = Column(String(128))
    inst_status = Column(SmallInteger)
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
