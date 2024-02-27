from sqlalchemy import Column
from sqlalchemy import String, Integer, DateTime, BigInteger
from ego.entity.base.BaseEntity import Base, BaseEntity


class ObjectDBDO(BaseEntity):
    __tablename__ = "object_db"

    db_type = Column(String(255), primary_key=True)
    db_instance = Column(String(255))
    db_port = Column(Integer)
    env = Column(String(20))
