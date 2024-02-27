from enum import Enum, unique


@unique
class OperateType(Enum):
    """
        数据操作类型
    """
    ADD = 0
    UPDATE = 1
    DELETE = 2

    description = {
        0: "新增",
        1: "更新",
        2: "删除",
    }
