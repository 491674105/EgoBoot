from sqlalchemy import Column
from sqlalchemy import SmallInteger, Integer, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudVolumeTypeDO(Base, BaseEntity):
    __tablename__ = "ops_cloud_volume_type"

    vt_id = Column(String(64), primary_key=True)
    cloud_id = Column(Integer)
    vt_extern_id = Column(String(64))
    vt_name = Column(String(64))
    priority = Column(Integer)
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
