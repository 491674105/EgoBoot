from enum import Enum, unique


@unique
class ServiceInstantStatus(Enum):
    """
        服务实例状态
    """
    DOWN = 0
    HEALTH = 1
    DELAY = 2
    UNKNOWN = -1

    description = {
        0: "服务宕机",
        1: "健康",
        2: "高延迟",
        -1: "初始化",
    }
