from sqlalchemy import Column
from sqlalchemy import SmallInteger, Integer, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsCloudCorpProjectDO(Base, BaseEntity):
    __tablename__ = "ops_cloud_corp_project"

    project_id = Column(String(64), primary_key=True)
    cloud_id = Column(Integer)
    domain_id = Column(String(64))
    project_extern_id = Column(String(64))
    project_extern_pid = Column(String(64))
    project_code = Column(String(32))
    project_name = Column(String(64))
    project_desc = Column(String(128))
    project_status = Column(SmallInteger)
    del_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
