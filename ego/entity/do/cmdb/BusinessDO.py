
from sqlalchemy import Column
from sqlalchemy import String, SmallInteger, BigInteger, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class BusinessDO(Base, BaseEntity):
    __tablename__ = "system_map"

    system_id = Column(BigInteger, primary_key=True, autoincrement=True)
    business_system = Column(String(255))
    bl_id = Column(BigInteger)
    del_flag = Column(SmallInteger)
    description = Column(String(255))
    create_time = Column(DateTime)
    update_time = Column(DateTime)
