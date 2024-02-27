from sqlalchemy import Column
from sqlalchemy import String, Integer, BigInteger, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OperateLogDO(Base, BaseEntity):
    __tablename__ = "operate_log"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uri = Column(String(255))
    endpoint = Column(String(255))
    table_name = Column(String(128))
    op_type = Column(Integer)
    host = Column(String(255))
    user_id = Column(BigInteger)
    operator = Column(String(64))
    op_time = Column(DateTime)
