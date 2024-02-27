from enum import Enum, unique


@unique
class ServiceStatus(Enum):
    """
        服务状态
    """
    WAIT = -1
    STARTUP = 1
    SLEEP = 2
    SHUTDOWN = 3

    description = {
        -1: "待上线",
        1: "使用中",
        2: "待下线",
        3: "已下线",
    }
