from sqlalchemy import Column
from sqlalchemy import BigInteger, String

from ego.entity.base.BaseEntity import Base, BaseEntity


class GitlabInfoDO(Base, BaseEntity):
    __tablename__ = "gitlab_info"

    project_id = Column(BigInteger, primary_key=True, autoincrement=True)
    uri = Column(String(255))
    http_uri = Column(String(255))
