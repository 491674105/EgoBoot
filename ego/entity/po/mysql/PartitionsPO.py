from sqlalchemy import Column
from sqlalchemy import String, BigInteger, DateTime, Text

from ego.entity.base.BaseEntity import Base, BaseEntity


class PartitionsPO(Base, BaseEntity):
    __tablename__ = "partitions"

    table_catalog = Column(String(512))
    table_schema = Column(String(64), primary_key=True)
    table_name = Column(String(64), primary_key=True)
    partition_name = Column(String(64), primary_key=True)
    subpartition_name = Column(String(64))
    partition_ordinal_position = Column(BigInteger)
    subpartition_ordinal_position = Column(BigInteger)
    partition_method = Column(String(18))
    subpartition_method = Column(String(12))
    partition_expression = Column(Text)
    subpartition_expression = Column(Text)
    partition_description = Column(Text)
    table_rows = Column(BigInteger)
    avg_row_length = Column(BigInteger)
    data_length = Column(BigInteger)
    max_data_length = Column(BigInteger)
    index_length = Column(BigInteger)
    data_free = Column(BigInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    check_time = Column(DateTime)
    checksum = Column(BigInteger)
    partition_comment = Column(String(80))
    nodegroup = Column(String(12))
    tablespace_name = Column(String(64))
