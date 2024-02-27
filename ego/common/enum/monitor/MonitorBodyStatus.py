from enum import Enum, unique


@unique
class MonitorBodyStatus(Enum):
    OK = 0
    PROBLEM = 1

    description = {
        0: "OK",
        1: "PROBLEM",
    }