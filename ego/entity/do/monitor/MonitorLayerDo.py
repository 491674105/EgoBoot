from sqlalchemy import Column
from sqlalchemy import String, Integer, BigInteger, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class MonitorLayerDo(Base, BaseEntity):
    __tablename__ = "layer"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    layered_id = Column(Integer)
    layered_name = Column(String(255))
    status = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)