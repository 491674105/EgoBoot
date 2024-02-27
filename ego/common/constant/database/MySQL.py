ADD_PARTITION = """
alter table [table_name] reorganize partition [max_partition_name] into
(
        partition [new_partition_name] values less than ([partition]),
        partition [max_partition_name] values less than maxvalue
);
"""

DROP_PARTITION = """
alter table [table_name] drop partition [partition_name];
"""
