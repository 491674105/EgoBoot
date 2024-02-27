from sqlalchemy import Column
from sqlalchemy import String, SmallInteger, BigInteger, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class ServiceAppSceneRelativeDO(Base, BaseEntity):
    __tablename__ = "service_app_scene_relative"

    relative_id = Column(String(64), primary_key=True)
    object_type = Column(SmallInteger)
    object_pk = Column(BigInteger)
    scene_id = Column(String(64))
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
