from sqlalchemy import Column
from sqlalchemy import String, Integer

from ego.entity.base.BaseEntity import Base, BaseEntity


class NacosNamespaceInfoDO(Base, BaseEntity):
    __tablename__ = "nacos_namespace_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(128))
    env = Column(String(16))
    namespace = Column(String(128))