from sqlalchemy import Column
from sqlalchemy import String, Text, Integer, Date

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudResourceBillExtraDO(Base, BaseEntity):
    __tablename__ = "ops_cloud_resource_bill_extra"

    bill_id = Column(String(64), primary_key=True)

    cloud_id = Column(Integer)
    zone_code = Column(String(64))
    bill_cycle_date = Column(Date, primary_key=True)
    resource_tag = Column(String(1024))
    project_id = Column(String(128))
    project_name = Column(String(256))
    formula = Column(Text)
