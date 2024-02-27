from sqlalchemy import Column
from sqlalchemy import String, Integer, BigInteger, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class MonitorLayerTimeLineDo(Base, BaseEntity):
    __tablename__ = "layer_timeline"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    layered_id = Column(Integer)
    class_id = Column(Integer)
    interface_id = Column(Integer)
    items_id = Column(Integer)
    host = Column(String(255))
    status = Column(Integer)
    priority_id = Column(Integer)
    description = Column(String(255))
    log_time = Column(DateTime)