from enum import Enum, unique


@unique
class MonitorClusterZone(Enum):
    shuitu = 0
    preprod = 1
    hwprod = 2
    zongbu = 3

    description = {
        0: "shuitu",
        1: "preprod",
        2: "hwprod",
        3: "zongbu"
    }
