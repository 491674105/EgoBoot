from sqlalchemy import Column
from sqlalchemy import SmallInteger, Integer, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudVpcDO(Base, BaseEntity):
    __tablename__ = "ops_cloud_vpc"

    vpc_id = Column(String(64), primary_key=True)
    vpc_extern_id = Column(String(64))
    vpc_name = Column(String(64))
    cloud_id = Column(Integer)
    zone_code = Column(String(64))
    network = Column(String(128))
    network_v6 = Column(String(128))
    vpc_status = Column(String(16))
    description = Column(String(255))
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
