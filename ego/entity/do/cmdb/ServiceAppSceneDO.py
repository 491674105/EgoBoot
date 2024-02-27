from sqlalchemy import Column
from sqlalchemy import String, SmallInteger, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class ServiceAppSceneDO(Base, BaseEntity):
    __tablename__ = "service_app_scene"

    scene_id = Column(String(64), primary_key=True)
    scene_name = Column(String(255))
    description = Column(String(255))
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
