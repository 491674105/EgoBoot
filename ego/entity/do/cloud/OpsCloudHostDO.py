from sqlalchemy import Column
from sqlalchemy import SmallInteger, Integer, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudHostDO(Base, BaseEntity):
    __tablename__ = "ops_cloud_host"

    host_id = Column(String(64), primary_key=True)
    host_extern_id = Column(String(64))
    host_full_id = Column(String(64))
    host_name = Column(String(128))
    description = Column(String(255))
    simple_code = Column(SmallInteger)
    spec_id = Column(String(64))
    img_id = Column(String(64))
    cloud_id = Column(Integer)
    zone_code = Column(String(64))
    avl_zone_code = Column(String(64))
    host_state = Column(String(32))
    launched_time = Column(DateTime)
    terminated_time = Column(DateTime)
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
