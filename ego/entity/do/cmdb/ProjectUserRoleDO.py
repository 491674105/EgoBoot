from sqlalchemy import Column
from sqlalchemy import String, SmallInteger, BigInteger, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class ProjectUserRoleDO(Base, BaseEntity):
    __tablename__ = "project_user_role"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    relative_type = Column(SmallInteger)
    system_id = Column(BigInteger)
    service_id = Column(BigInteger)
    user_info_type = Column(SmallInteger)
    user_id = Column(BigInteger)
    user_name = Column(String(64))
    role_id = Column(BigInteger)
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
