from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class SqlWorkflow(Base, BaseEntity):
    __tablename__ = "sql_workflow"
    id = Column(Integer, primary_key=True, autoincrement=True)
    workflow_name = Column(String(50))
    demand_url = Column(String(500))
    group_id = Column(Integer)
    group_name = Column(String(100))
    db_name = Column(String(64))
    syntax_type = Column(Integer)
    is_backup = Column(Integer)
    engineer = Column(String(30))
    engineer_display = Column(String(50))
    status = Column(String(50))
    audit_auth_groups = Column(String(255))
    run_date_start = Column(DateTime)
    run_date_end = Column(DateTime)
    create_time = Column(DateTime)
    finish_time = Column(DateTime)
    is_manual = Column(Integer)
    instance_id = Column(Integer)

