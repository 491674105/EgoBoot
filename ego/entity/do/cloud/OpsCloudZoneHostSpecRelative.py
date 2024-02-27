from sqlalchemy import Column
from sqlalchemy import SmallInteger, Integer, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudZoneHostSpecRelative(Base, BaseEntity):
    __tablename__ = "ops_cloud_zone_host_spec_relative"

    relative_id = Column(String(64), primary_key=True)
    cloud_id = Column(Integer)
    zone_code = Column(String(64))
    avl_zone_code = Column(String(64))
    spec_extern_id = Column(String(64))
    spec_status = Column(String(16))
    az_spec_status = Column(String(16))
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
