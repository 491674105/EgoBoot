from sqlalchemy import Column
from sqlalchemy import String, Integer, DateTime, BigInteger
from ego.entity.base.BaseEntity import Base, BaseEntity


class ConfSoftdelTempDO(Base, BaseEntity):
    __tablename__ = "conf_softdel_temp"

    kid = Column(BigInteger, primary_key=True)
    config_id = Column(BigInteger, primary_key=True)
    del_flag = Column(Integer)
