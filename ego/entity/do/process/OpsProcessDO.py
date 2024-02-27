from sqlalchemy import Column
from sqlalchemy import SmallInteger, BigInteger, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsProcessDO(Base, BaseEntity):
    __tablename__ = "ops_process"

    process_id = Column(BigInteger, primary_key=True, autoincrement=True)
    process_no = Column(String(64))
    process_definition_id = Column(String(64))
    process_instance_id = Column(String(64))
    process_theme = Column(String(64))
    originator_id = Column(BigInteger)
    originator = Column(String(64))
    process_status = Column(SmallInteger)
    process_type_id = Column(BigInteger)
    mark = Column(String(255))
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
