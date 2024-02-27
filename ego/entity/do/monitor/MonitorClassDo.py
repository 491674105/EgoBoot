from sqlalchemy import Column
from sqlalchemy import String, Integer, BigInteger, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class MonitorClassDo(Base, BaseEntity):
    __tablename__ = "class_layer"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    layered_id = Column(Integer)
    class_id = Column(Integer)
    class_name = Column(String(255))
    status = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)