from sqlalchemy import Column
from sqlalchemy import SmallInteger, Integer, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudImageDO(Base, BaseEntity):
    __tablename__ = "ops_cloud_image"

    image_id = Column(String(64), primary_key=True)
    cloud_id = Column(Integer)
    image_extern_id = Column(String(64))
    image_type = Column(String(16))
    image_name = Column(String(128))
    os_type = Column(String(16))
    platform = Column(String(64))
    os_bit = Column(Integer)
    os_version = Column(String(64))
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
