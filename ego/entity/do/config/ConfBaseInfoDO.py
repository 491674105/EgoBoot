from sqlalchemy import Column
from sqlalchemy import String, Integer, DateTime, BigInteger
from ego.entity.base.BaseEntity import Base, BaseEntity


class ConfBaseInfoDo(Base):
    __tablename__ = "conf_base_info"

    config_id = Column(BigInteger, primary_key=True, autoincrement=True)
    conf_basename = Column(String(255))
    conf_type = Column(String(255))
    conf_fullname = Column(String(255))
    env = Column(String(16))
    iscommon = Column(BigInteger)
    del_flag = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
