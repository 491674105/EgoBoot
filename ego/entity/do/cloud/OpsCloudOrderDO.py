from sqlalchemy import Column
from sqlalchemy import SmallInteger, Integer, DECIMAL, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudOrderDO(Base, BaseEntity):
    __tablename__ = "ops_cloud_order"

    order_id = Column(String(64), primary_key=True)

    cloud_id = Column(Integer)
    service_type_code = Column(String(128))
    service_type_name = Column(String(200))
    order_extern_id = Column(String(64))
    order_source = Column(SmallInteger)
    order_status = Column(SmallInteger)
    order_type = Column(SmallInteger)
    contract_id = Column(String(64))

    currency_code = Column(String(8))
    unit_code = Column(SmallInteger)
    order_amount = Column(DECIMAL(32, 8))
    discounted_price = Column(DECIMAL(32, 8))

    cash_coupon = Column(DECIMAL(32, 8))
    allowance_coupon = Column(DECIMAL(32, 8))
    stored_card_coupon = Column(DECIMAL(32, 8))
    commission = Column(DECIMAL(32, 8))
    consumption_coupon = Column(DECIMAL(32, 8))

    pay_time = Column(DateTime)

    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
