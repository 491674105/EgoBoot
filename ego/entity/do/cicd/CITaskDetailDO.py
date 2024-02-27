from sqlalchemy import Column
from sqlalchemy import String, BigInteger, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class CITaskDetailDO(Base, BaseEntity):
    __tablename__ = "ci_task_detail"

    task_id = Column(BigInteger, primary_key=True, autoincrement=True)
    system_id = Column(String(256))
    service = Column(String(64))
    env = Column(String(32))
    deploy_tag = Column(String(60))
    deploy_status = Column(String(16))
    deploy_to_server = Column(String(256))
    service_port = Column(String(6))
    deploy_time = Column(DateTime)
    rollback_tag = Column(String(256))
    rollback_time = Column(String(256))
    mark = Column(String(256))
