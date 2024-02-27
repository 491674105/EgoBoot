from sqlalchemy import Column
from sqlalchemy import String, Integer, DateTime, BigInteger
from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsJumpResIdMapDo(Base):
    __tablename__ = "ops_jump_res_id_map"

    map_id = Column(String(64), primary_key=True)
    cmdb_res_node_id = Column(String(64))
    cmdb_res_node_name = Column(String(64))
    cmdb_res_node_type = Column(Integer)
    jump_assets_node_id = Column(String(64))
    par_jump_assets_node_id = Column(String(64))
    cloud_id = Column(Integer())
    zone_code = Column(String(64))
    del_flag = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)