from sqlalchemy import Column
from sqlalchemy import SmallInteger, Integer, String

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudVTZoneRelative(Base, BaseEntity):
    __tablename__ = "ops_cloud_vt_zone_relative"

    relative_id = Column(String(64), primary_key=True)
    cloud_id = Column(Integer)
    vt_extern_id = Column(String(64))
    zone_code = Column(String(64))
    avl_zone_code = Column(String(64))
    is_valid = Column(SmallInteger)
    is_sold_out = Column(SmallInteger)
