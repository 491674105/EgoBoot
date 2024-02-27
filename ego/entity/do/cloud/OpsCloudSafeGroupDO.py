from sqlalchemy import Column
from sqlalchemy import SmallInteger, Integer, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudSafeGroupDO(Base, BaseEntity):
    __tablename__ = "ops_cloud_safe_group"

    sg_id = Column(String(64), primary_key=True)
    sg_extern_id = Column(String(64))
    sg_name = Column(Integer)
    cloud_id = Column(String(64))
    zone_code = Column(String(64))
    description = Column(String(255))
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
