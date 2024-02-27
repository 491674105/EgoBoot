from sqlalchemy import Column
from sqlalchemy import String, Integer, DateTime, BigInteger, TEXT
from ego.entity.base.BaseEntity import Base, BaseEntity


class ConfPermissionAssociationsDO(Base, BaseEntity):
    __tablename__ = "conf_permission_associations"

    pid = Column(BigInteger, primary_key=True, autoincrement=True)
    kid = Column(BigInteger)
    role_id = Column(String(20))
    del_flag = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
