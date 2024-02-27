from sqlalchemy import Column
from sqlalchemy import Integer

from ego.entity.base.BaseEntity import Base, BaseEntity


class PortsDO(Base, BaseEntity):
    __tablename__ = "ports"

    port = Column(Integer, primary_key=True)
    type = Column(Integer)
    status = Column(Integer)
    reuse = Column(Integer)
