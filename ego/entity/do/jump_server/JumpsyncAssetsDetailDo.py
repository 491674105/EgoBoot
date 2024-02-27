from sqlalchemy import Column
from sqlalchemy import String, Integer, DateTime, BigInteger
from ego.entity.base.BaseEntity import Base, BaseEntity


class JumpsyncAssetsDetailDo(Base):
    __tablename__ = "jumpsync_assets_detail"

    id = Column(String(128), primary_key=True)
    host_name = Column(String(128))
    addr4 = Column(String(20), primary_key=True)
    jms_env = Column(String(20))
    host_extern_id = Column(String(64))
    zone_code = Column(String(64))
    terminated_time = Column(DateTime)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    del_status = Column(Integer)
    msg = Column(String(10))
    cloud_id = Column(Integer)