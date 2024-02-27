from sqlalchemy import Column
from sqlalchemy import String, Integer, DateTime, BigInteger
from ego.entity.base.BaseEntity import Base, BaseEntity


class ConfKeysDO(Base, BaseEntity):
    __tablename__ = "conf_keys"

    kid = Column(BigInteger, primary_key=True, autoincrement=True)
    key = Column(String(255))
    del_flag = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
