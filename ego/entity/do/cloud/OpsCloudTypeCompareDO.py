from sqlalchemy import Column
from sqlalchemy import SmallInteger, Integer, String

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudTypeCompareDO(Base, BaseEntity):
    __tablename__ = "ops_cloud_class_compare"

    class_id = Column(String(64), primary_key=True)
    cloud_id = Column(Integer)
    class_type = Column(String(32))
    cloud_class = Column(String(32))
    cloud_num_flag = Column(SmallInteger)
    local_class = Column(String(32))
    local_num_flag = Column(SmallInteger)
    description = Column(String(128))
