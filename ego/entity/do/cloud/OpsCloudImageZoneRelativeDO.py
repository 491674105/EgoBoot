from sqlalchemy import Column
from sqlalchemy import SmallInteger, Integer, String

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudImageZoneRelativeDO(Base, BaseEntity):
    __tablename__ = "ops_cloud_image_zone_relative"

    relative_id = Column(String(64), primary_key=True)
    cloud_id = Column(Integer)
    zone_code = Column(String(64))
    image_extern_id = Column(String(64))
    img_status = Column(String(16))
    charge_flag = Column(SmallInteger)
