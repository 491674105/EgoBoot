from enum import Enum, unique


@unique
class MonitorPriority(Enum):
    UNKNOWN = 0
    INFORMATION = 1
    WARNING = 2
    AVERAGE = 3
    HIGH = 4
    DISASTER = 5


    description = {
        0: "未分配",
        1: "信息",
        2: "警告",
        3: "一般严重",
        4: "严重",
        5: "灾难"
    }