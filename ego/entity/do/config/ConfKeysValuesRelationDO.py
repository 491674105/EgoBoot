from sqlalchemy import Column
from sqlalchemy import String, Integer, DateTime, BigInteger
from ego.entity.base.BaseEntity import Base, BaseEntity


class ConfKeysValuesRelationDO(Base, BaseEntity):
    __tablename__ = "conf_keys_values_relation"

    config_id = Column(BigInteger, primary_key=True)
    kid = Column(BigInteger, primary_key=True)
    value = Column(String(20480))
    del_flag = Column(Integer)
    mark = Column(String(255))
    create_time = Column(DateTime)
    update_time = Column(DateTime)
