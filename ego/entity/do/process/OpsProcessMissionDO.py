from sqlalchemy import Column
from sqlalchemy import BigInteger, SmallInteger, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsProcessMissionDO(Base, BaseEntity):
    __tablename__ = "ops_process_mission"

    mission_id = Column(BigInteger, primary_key=True, autoincrement=True)
    mission_no = Column(String(64))
    parent_mission_no = Column(String(64))
    process_id = Column(BigInteger)
    process_no = Column(String(64))
    execution_id = Column(String(64))
    mission_definition_id = Column(String(64))
    mission_definition_key = Column(String(64))
    mission_definition_name = Column(String(128))
    mission_status = Column(SmallInteger)
    role_id = Column(BigInteger)
    user_name = Column(String(64))
    description = Column(String(255))
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
