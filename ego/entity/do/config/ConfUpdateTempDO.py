from sqlalchemy import Column
from sqlalchemy import String, Integer, DateTime, BigInteger
from ego.entity.base.BaseEntity import Base, BaseEntity


class ConfUpdateTempDO(Base, BaseEntity):
    __tablename__ = "conf_update_temp"

    kid = Column(BigInteger, primary_key=True)
    config_id = Column(BigInteger, primary_key=True)
    value = Column(String(20480))
