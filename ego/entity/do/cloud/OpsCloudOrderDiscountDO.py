from sqlalchemy import Column
from sqlalchemy import Integer, DECIMAL, String

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudOrderDiscountDO(Base, BaseEntity):
    __tablename__ = "ops_cloud_order_discount"

    discount_id = Column(String(64), primary_key=True)

    cloud_id = Column(Integer)
    order_extern_id = Column(String(64))
    discount_type = Column(String(16))
    discount_amount = Column(DECIMAL(32, 8))
