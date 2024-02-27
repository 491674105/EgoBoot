from sqlalchemy import Column
from sqlalchemy import SmallInteger, Integer, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudImageTypeDO(Base, BaseEntity):
    __tablename__ = "ops_cloud_image_type"

    it_id = Column(String(64), primary_key=True)
    cloud_id = Column(Integer)
    image_type = Column(String(16))
    description = Column(String(64))
    has_os_type = Column(SmallInteger)
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
