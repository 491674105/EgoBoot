from sqlalchemy import Column
from sqlalchemy import Integer, BigInteger, String

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudSyncTimestampDO(Base, BaseEntity):
    __tablename__ = "ops_cloud_sync_timestamp"

    sync_id = Column(BigInteger, autoincrement=True, primary_key=True)
    sync_tb_name = Column(String(64))
    cloud_id = Column(Integer)
    sync_tp = Column(BigInteger)
