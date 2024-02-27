
from sqlalchemy import Column
from sqlalchemy import String, SmallInteger, BigInteger, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class BusinessLineDO(Base, BaseEntity):
    __tablename__ = "business_line_info"

    bl_id = Column(BigInteger, primary_key=True, autoincrement=True)
    business_line = Column(String(64))
    mark = Column(String(255))
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
