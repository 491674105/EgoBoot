from sqlalchemy import Column
from sqlalchemy import String, Integer, DateTime, BigInteger
from ego.entity.base.BaseEntity import Base, BaseEntity


class MiddlewareDO(BaseEntity):
    __tablename__ = "middleware"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    servicename = Column(String(255))
    healthy_instance = Column(String(255))
    port = Column(Integer)
    env = Column(String(16))
    status = Column(Integer)
    del_flag = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
