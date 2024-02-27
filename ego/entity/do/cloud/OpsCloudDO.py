from sqlalchemy import Column
from sqlalchemy import SmallInteger, BigInteger, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudDO(Base, BaseEntity):
    __tablename__ = "ops_cloud"

    cloud_id = Column(BigInteger, autoincrement=True, primary_key=True)
    cloud_name = Column(String(32))
    description = Column(String(256))
    las_sync_time = Column(BigInteger)
    use_admin = Column(SmallInteger)
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
