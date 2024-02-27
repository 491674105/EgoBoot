from sqlalchemy import Column
from sqlalchemy import SmallInteger, Integer, BigInteger, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudHostSpecDO(Base, BaseEntity):
    __tablename__ = "ops_cloud_host_spec"

    spec_id = Column(String(64), primary_key=True)
    cloud_id = Column(Integer)
    spec_extern_id = Column(String(64))
    spec_name = Column(String(64))
    cpus = Column(Integer)
    vcpus = Column(Integer)
    ram = Column(BigInteger)
    disk = Column(BigInteger)
    swap = Column(String(32))
    cpu_spec = Column(String(64))
    cpu_architecture = Column(String(64))
    gpu_spec = Column(String(64))
    charge_type = Column(String(16))
    min_bandwidth = Column(BigInteger)
    max_bandwidth = Column(BigInteger)
    max_pps = Column(BigInteger)
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
