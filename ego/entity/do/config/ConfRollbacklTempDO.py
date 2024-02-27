from sqlalchemy import Column
from sqlalchemy import String, Integer, DateTime, BigInteger
from ego.entity.base.BaseEntity import Base, BaseEntity


class ConfRollbackTempDO(Base, BaseEntity):
    __tablename__ = "conf_rollback_temp"

    kid = Column(BigInteger, primary_key=True)
    cid = Column(BigInteger, primary_key=True)
    service_id = Column(BigInteger, primary_key=True)
    conf_fullname = Column(String(255))
    key = Column(String(255))
    value = Column(String(20480))
    service_name = Column(String(255))
    conf_type = Column(String(255))