from sqlalchemy import Column
from sqlalchemy import BigInteger, Integer, String

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudSyncMetaApiDO(Base, BaseEntity):
    __tablename__ = "ops_cloud_sync_meta_api"

    api_id = Column(BigInteger, autoincrement=True, primary_key=True)
    cloud_id = Column(Integer)
    uri = Column(String(256))
    api_method = Column(String(16))
    description = Column(String(256))
