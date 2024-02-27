from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, DateTime, Enum
from sqlalchemy.orm import relationship

from ego.entity.base.BaseEntity import Base, BaseEntity
import datetime


class ArcheryTask(Base, BaseEntity):
    __tablename__ = "archery_task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    env = Column(String)
    process_id = Column(Integer)
    task_id = Column(Integer)
    se_plan_id = Column(Integer)
    archery_workflow_id = Column(Integer)
    callback_func = Column(String)
    callback_type = Column(String)
    status = Column(Integer)
    task_begin_time = Column(DateTime)
    task_end_time = Column(DateTime)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    mission_no = Column(String)


class DBInstance(Base, BaseEntity):
    __tablename__ = "db_instance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    host_id = Column(Integer)
    cluster_id = Column(Integer)
    port = Column(Integer)
    status = Column(Integer)
    role = Column(Enum("master", "slave", "single"))
    description = Column(String(255))
    create_time = Column(DateTime)
    update_time = Column(DateTime)

class DBSchema(Base, BaseEntity):
    __tablename__ = "db_schema"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(String(100))
    instance_id = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)


class DBInsCluster(Base, BaseEntity):
    __tablename__ = "db_ins_cluster"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    env = Column(Integer)
    db_type = Column(Enum('mysql', 'sqlserver', 'oracle', 'mongo'), server_default='mysql')
    status = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)

    # env_r = relationship("DBInstanceENV", back_populates="instance")


class DBInstanceENV(Base, BaseEntity):
    __tablename__ = "instance_env"
    id = Column(Integer, primary_key=True, autoincrement=True)
    env = Column(String(16))
    description = Column(String(128))

    # instance = relationship("DBInsCluster")


class ArcheryOPSLog(Base, BaseEntity):
    __tablename__ = "archery_ops_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    env = Column(String)
    process_id = Column(Integer)
    task_id = Column(Integer)
    se_plan_id = Column(Integer)
    archery_workflow_ids = Column(String)
    stage = Column(String)
    status = Column(String)
    info = Column(String)
    # create_time = Column(DateTime)
    # update_time = Column(DateTime)


class DBHosts(Base, BaseEntity):
    __tablename__ = "db_hosts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(15))
    vip = Column(String(200))
    specs = Column(String(255))
    region = Column(Enum('重庆总部机房', '水土腾龙机房', '华为云北京一区可用区1', '华为云北京一区可用区2', '华为云北京一区可用区3',
                         '华为云北京四区可用区1', '华为云北京四区可用区2', '华为云北京四区可用区3', '华为云北京四区可用区7', '阿里云'))
    type = Column(Enum('ECS', 'RDS', 'PM', 'VM'))
    login_type = Column(Enum('VNC', 'RPC', 'SSH', 'JUMP', '华为云'))
    description = Column(String)


class DBInstanceArcheryMap(Base, BaseEntity):
    __tablename__ = "db_instance_archery_map"
    id = Column(Integer, primary_key=True, autoincrement=True)
    db_instance_id = Column(Integer)
    archery_instance_id = Column(Integer)

