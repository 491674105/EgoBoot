
from sqlalchemy import Column
from sqlalchemy import String, Integer, SmallInteger

from ego.entity.base.BaseEntity import Base, BaseEntity


class AlertUserDO(Base, BaseEntity):
    __tablename__ = "alert_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    alert_group = Column(String(16))
    user_name = Column(String(255))
    bussiness = Column(String(255))
    uplevel_2 = Column(String(255))
    uplevel_3 = Column(String(255))
