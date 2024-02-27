from enum import Enum, unique


@unique
class ServiceFlag(Enum):
    """
        服务标识
    """
    POSITIVE = 0
    NEGATIVE = 1
    PLAN = 2

    description = {
        0: "允许下线",
        1: "不可下线",
        2: "计划下线",
    }
