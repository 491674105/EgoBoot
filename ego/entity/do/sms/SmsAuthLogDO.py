from sqlalchemy import Column
from sqlalchemy import String, BigInteger, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class SmsAuthLogDO(Base, BaseEntity):
    __tablename__ = "sms_auth_log"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    receiver = Column(String(64))
    code_number = Column(String(16))
    send_time = Column(DateTime)
    msg_id = Column(String(255))
    send_status = Column(String(64))