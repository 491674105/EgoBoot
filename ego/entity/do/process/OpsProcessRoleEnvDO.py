from sqlalchemy import Column
from sqlalchemy import SmallInteger, BigInteger, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsProcessRoleEnvDO(Base, BaseEntity):
    __tablename__ = "ops_process_publish_role_env"

    role_env_id = Column(BigInteger, primary_key=True, autoincrement=True)
    role_id = Column(BigInteger)
    env_type = Column(SmallInteger)
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
