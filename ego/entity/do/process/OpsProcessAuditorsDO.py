from sqlalchemy import Column
from sqlalchemy import Integer, BigInteger, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsProcessAuditorsDO(Base, BaseEntity):
    __tablename__ = "ops_process_auditors"

    auditor_id = Column(BigInteger, primary_key=True, autoincrement=True)
    process_id = Column(BigInteger)
    process_no = Column(String(64))
    task_definition_key = Column(String(64))
    task_definition_name = Column(String(128))
    user_id = Column(BigInteger)
    user_name = Column(String(64))
    alias = Column(String(64))
    role_id = Column(BigInteger)
    del_flag = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
