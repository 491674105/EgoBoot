from sqlalchemy import Column
from sqlalchemy import SmallInteger, Integer, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudAvlZoneDO(Base, BaseEntity):
    __tablename__ = "ops_cloud_avl_zone"
    az_id = Column(String(64), primary_key=True)
    cloud_id = Column(Integer)
    zone_code = Column(String(64))
    avl_zone_code = Column(String(64))
    simple_code = Column(SmallInteger)
    avl_zone_status = Column(SmallInteger)
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
