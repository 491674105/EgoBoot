from sqlalchemy import Column
from sqlalchemy import String, SmallInteger, Integer, BigInteger, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class PublishLogDO(Base, BaseEntity):
    __tablename__ = "publish_log"

    publish_id = Column(String(64), primary_key=True)
    publish_source = Column(SmallInteger)
    business_key = Column(String(64))
    service_id = Column(BigInteger)
    inst_id = Column(BigInteger)
    publish_subject = Column(Integer)
    publish_method = Column(String(16))
    env = Column(String(16))
    xxf_zone = Column(String(16))
    publish_tag = Column(String(128))
    commit_id = Column(String(64))
    status = Column(Integer)
    publish_user_id = Column(BigInteger)
    publish_user = Column(String(64))
    publish_time = Column(DateTime)
    finish_time = Column(DateTime)
    mark = Column(String(255))
