from sqlalchemy import Column
from sqlalchemy import SmallInteger, Integer, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudZoneDO(Base, BaseEntity):
    __tablename__ = "ops_cloud_zone"

    zone_id = Column(String(64), primary_key=True)
    cloud_id = Column(Integer)
    zone_code = Column(String(64))
    simple_code = Column(SmallInteger)
    zh_cn = Column(String(128))
    en_us = Column(String(128))
    pt_br = Column(String(128))
    es_us = Column(String(128))
    es_es = Column(String(128))
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
