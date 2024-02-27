from sqlalchemy import Column
from sqlalchemy import SmallInteger, Integer, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudHostNCDO(Base, BaseEntity):
    __tablename__ = "ops_cloud_host_nc"

    nc_id = Column(String(64), primary_key=True)
    vpc_extern_id = Column(String(64))
    cloud_id = Column(Integer)
    host_extern_id = Column(String(64))

    addr4 = Column(String(32))
    addr6 = Column(String(64))
    mac = Column(String(32))

    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
