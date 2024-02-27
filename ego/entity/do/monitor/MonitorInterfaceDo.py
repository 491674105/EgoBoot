from sqlalchemy import Column
from sqlalchemy import String, Integer, BigInteger, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class MonitorInterfaceDo(Base, BaseEntity):
    __tablename__ = "interface_layer"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    class_id = Column(BigInteger)
    interface_id = Column(BigInteger)
    interface_name = Column(String(255))
    status = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)