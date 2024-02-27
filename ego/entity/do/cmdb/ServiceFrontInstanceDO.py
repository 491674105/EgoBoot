from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, BigInteger, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class ServiceFrontInstanceDO(Base, BaseEntity):
    __tablename__ = "front_info"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    front_nodes = Column(String(255))
    front_env = Column(String(255))
    build_cmd = Column(String(255))
    fid = Column(BigInteger, ForeignKey("service_info.service_id"))
    cdnurl = Column(String(255))
    status = Column(Integer)
    del_flag = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
