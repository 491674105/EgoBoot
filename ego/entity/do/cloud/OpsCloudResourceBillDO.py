from sqlalchemy import Column
from sqlalchemy import SmallInteger, Integer, DECIMAL, String, Date, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudResourceBillDO(Base, BaseEntity):
    __tablename__ = "ops_cloud_resource_bill"

    bill_id = Column(String(64), primary_key=True)

    cloud_id = Column(Integer)
    zone_code = Column(String(64))
    order_extern_id = Column(String(64))
    trade_id = Column(String(64))
    currency_code = Column(String(8))
    currency_unit_code = Column(SmallInteger)

    bill_cycle_date = Column(Date, primary_key=True)
    bill_type = Column(SmallInteger)
    period_type = Column(SmallInteger)
    customer_id = Column(String(64))

    service_type_code = Column(String(256))
    service_type_name = Column(String(256))
    resource_type_code = Column(String(128))
    resource_type_name = Column(String(200))

    resource_id = Column(String(128))
    resource_name = Column(String(128))
    sku_code = Column(String(64))

    usage_type = Column(String(24))
    usages = Column(DECIMAL(32, 8))
    usage_unit_code = Column(SmallInteger)
    package_usage = Column(DECIMAL(32, 8))
    package_usage_unit_code = Column(SmallInteger)
    reserve_usage = Column(DECIMAL(32, 8))
    reserve_usage_unit_code = Column(SmallInteger)

    charge_mode = Column(SmallInteger)
    unit_price = Column(DECIMAL(32, 8))
    price_unit = Column(String(64))
    official = Column(DECIMAL(32, 8))
    discount = Column(DECIMAL(32, 8))
    amount = Column(DECIMAL(32, 8))
    cash = Column(DECIMAL(32, 8))
    credit_limit = Column(DECIMAL(32, 8))
    allowance_coupon = Column(DECIMAL(32, 8))
    cash_coupon = Column(DECIMAL(32, 8))
    stored_card_coupon = Column(DECIMAL(32, 8))
    bonus = Column(DECIMAL(32, 8))
    debt = Column(DECIMAL(32, 8))
    adjustment = Column(DECIMAL(32, 8))

    product_spec_desc = Column(String(256))

    start_time = Column(DateTime)
    end_time = Column(DateTime)

    create_time = Column(DateTime)
    update_time = Column(DateTime)
