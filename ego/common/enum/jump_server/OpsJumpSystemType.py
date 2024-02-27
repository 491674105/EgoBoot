from enum import Enum, unique


@unique
class OpsJumpSystemType(Enum):
    """
        系统业务线类型
    """
    BUSINESS_LINE = 1
    BUSINESS_SYSTEM = 2
    HOST = 3

    description = {
        1: "业务线",
        2: "业务系统",
        3: "服务器"
    }