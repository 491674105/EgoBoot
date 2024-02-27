from enum import Enum, unique


@unique
class MonitorStatus(Enum):
    GREEN = 0
    YELLOW = 1
    RED = 2


    description = {
        0: "正常",
        1: "警告",
        2: "异常"
    }