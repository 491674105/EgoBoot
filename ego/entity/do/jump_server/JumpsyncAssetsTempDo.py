from sqlalchemy import Column
from sqlalchemy import String, Integer, DateTime, BigInteger
from ego.entity.base.BaseEntity import Base, BaseEntity


class JumpsyncAssetsTempDo(Base):
    __tablename__ = "jumpsync_assets_temp"

    id = Column(String(128), primary_key=True)
    ip = Column(String(20), primary_key=True)
    jms_env = Column(String(20))