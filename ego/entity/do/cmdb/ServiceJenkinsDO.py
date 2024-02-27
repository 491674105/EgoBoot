from sqlalchemy import Column
from sqlalchemy import String, SmallInteger, BigInteger, Text, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class ServiceJenkinsDO(Base, BaseEntity):
    __tablename__ = "service"

    service_id = Column(BigInteger, primary_key=True, autoincrement=True)
    business_system = Column(String(255))
    service_name = Column(String(255))
    port = Column(String(255))
    service_user_id = Column(BigInteger)
    deployment_master = Column(String(255))
    testing_user_id = Column(BigInteger)
    testing_user = Column(String(255))
    system_id = Column(BigInteger)
    service_type = Column(String(30))
    flag = Column(SmallInteger)
    status = Column(SmallInteger)
    mark = Column(Text)
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)

