from sqlalchemy import Column, ForeignKey
from sqlalchemy import BigInteger, String

from ego.entity.base.BaseEntity import Base, BaseEntity


class ServiceGitDO(Base, BaseEntity):
    __tablename__ = "service_git"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    project_id = Column(BigInteger)
    uri = Column(String(255))
    http_uri = Column(String(255))
    service_id = Column(BigInteger, ForeignKey("service_info.service_id"))
