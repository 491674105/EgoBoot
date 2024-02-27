from sqlalchemy import Column
from sqlalchemy import SmallInteger, BigInteger, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsProcessRolePermissionDO(Base, BaseEntity):
    __tablename__ = "ops_process_role_permission"

    permission_id = Column(BigInteger, primary_key=True, autoincrement=True)
    role_id = Column(BigInteger)
    step_id = Column(BigInteger)
    resource_id = Column(BigInteger)
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
