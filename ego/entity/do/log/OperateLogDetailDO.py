from sqlalchemy import Column
from sqlalchemy import BigInteger, Text

from ego.entity.base.BaseEntity import Base, BaseEntity


class OperateLogDetailDO(Base, BaseEntity):
    __tablename__ = "operate_log_detail"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    log_id = Column(BigInteger)
    description = Column(Text)
    detail = Column(Text)
