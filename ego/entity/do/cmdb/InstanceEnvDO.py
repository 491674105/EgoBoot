from sqlalchemy import Column
from sqlalchemy import String, Integer, SmallInteger

from ego.entity.base.BaseEntity import Base, BaseEntity


class InstanceEnvDO(Base, BaseEntity):
    __tablename__ = "instance_env"

    id = Column(Integer, primary_key=True, autoincrement=True)
    env = Column(String(16))
    env_type = Column(SmallInteger)
    simple_code = Column(String(2))
    description = Column(String(128))
