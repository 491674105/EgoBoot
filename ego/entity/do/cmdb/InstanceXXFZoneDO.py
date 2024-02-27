
from sqlalchemy import Column
from sqlalchemy import String, Integer

from ego.entity.base.BaseEntity import Base, BaseEntity


class InstanceXXFZoneDO(Base, BaseEntity):
    __tablename__ = "instance_xxf_zone"

    id = Column(Integer, primary_key=True, autoincrement=True)
    zone = Column(String(32))
    description = Column(String(128))
