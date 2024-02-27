from sqlalchemy import Column
from sqlalchemy import String, Integer, BigInteger, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class UploadParamtersDO(Base, BaseEntity):
    __tablename__ = "upload_paramters"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    service_id = Column(BigInteger)
    ci_class = Column(String(255))
    ci_starter = Column(String(64))
    cd_class = Column(String(255))
    cd_starter = Column(String(64))
    notice_class = Column(String(255))
    notice_starter = Column(String(64))
    upload_params = Column(String(255))
    flag = Column(Integer)
    status = Column(Integer)
    del_flag = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
