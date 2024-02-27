from enum import Enum, unique


@unique
class OpsProcessErrorLevel(Enum):
    """
        流程异常级别
    """
    FIRST = 1
    SECOND = 2
