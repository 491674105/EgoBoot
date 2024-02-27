from sqlalchemy import Column
from sqlalchemy import SmallInteger, Integer, BigInteger, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudSubNetworkDO(Base, BaseEntity):
    __tablename__ = "ops_cloud_sub_network"

    sn_id = Column(String(64), primary_key=True)

    sn_extern_id = Column(String(64))
    sn_name = Column(String(64))
    vpc_extern_id = Column(String(64))
    cloud_id = Column(Integer)
    zone_code = Column(String(64))
    avl_zone_code = Column(String(64))
    sub_network = Column(String(128))
    gateway = Column(String(32))
    sub_network_v6 = Column(String(128))
    gateway_v6 = Column(String(128))
    dhcp = Column(SmallInteger)
    dns1 = Column(String(32))
    dns2 = Column(String(32))
    sn_status = Column(String(16))
    description = Column(String(255))
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
