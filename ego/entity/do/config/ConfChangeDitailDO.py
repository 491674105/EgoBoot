from sqlalchemy import Column
from sqlalchemy import String, Integer, DateTime, BigInteger
from ego.entity.base.BaseEntity import Base, BaseEntity


class ConfChangeDitailDO(Base, BaseEntity):
    __tablename__ = "conf_change_ditail"

    id = Column(BigInteger, primary_key=True, autoincrement=Tru)
    worker_number = Column(String(255))
    employee_name = Column(String(255))
    conf_fullname = Column(String(255))
    config_id = Column(BigInteger)
    env = Column(String(20))
    modification_time = Column(DateTime)
