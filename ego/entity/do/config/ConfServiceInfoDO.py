from sqlalchemy import Column
from sqlalchemy import String, Integer, DateTime, BigInteger
from ego.entity.base.BaseEntity import Base, BaseEntity


class ConfServiceInfoDO(Base, BaseEntity):
    __tablename__ = "conf_service_info"

    cid = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(BigInteger)
    config_id = Column(BigInteger)
    # conf_basename = Column(String(255))
    # conf_type = Column(String(255))
    # conf_fullname = Column(String(255))
    # env = Column(String(16))
    # iscommon = Column(BigInteger)
    del_flag = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
