from sqlalchemy import Column
from sqlalchemy import Integer, BigInteger, String, DateTime, SmallInteger

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsProcessPublishTaskDO(Base, BaseEntity):
    __tablename__ = "ops_process_publish_task"

    task_id = Column(BigInteger, primary_key=True, autoincrement=True)
    task_no = Column(String(64))
    process_id = Column(BigInteger)
    process_no = Column(String(64))
    task_priority = Column(Integer)
    system_id = Column(BigInteger)
    business_system = Column(String(64))
    service_id = Column(BigInteger)
    service_name = Column(String(64))
    service_type = Column(String(10))
    publish_method = Column(String(16))
    xxf_zone = Column(String(16))
    publish_tag = Column(String(128))
    operator_id = Column(BigInteger)
    operator = Column(String(64))
    status = Column(SmallInteger)
    mark = Column(String(255))
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
