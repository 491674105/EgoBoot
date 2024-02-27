from enum import Enum, unique


@unique
class MiddleWareStatus(Enum):
    """
        中间件实例状态
    """
    SHUTDOWN = 0
    STARTUP = 1

    description = {
        0: "下线",
        1: "上线",
    }
