from sqlalchemy import Column
from sqlalchemy import SmallInteger, Integer, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudImageOSTypeDO(Base, BaseEntity):
    __tablename__ = "ops_cloud_image_os_type"

    ot_id = Column(String(64), primary_key=True)
    cloud_id = Column(Integer)
    os_type = Column(String(16))
    platform = Column(String(64))
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
