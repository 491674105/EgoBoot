from enum import Enum, unique


@unique
class OpsSqlExecStatus(Enum):
    """
        SQL执行计划状态
    """
    INIT = -1
    COMMITTED = 1
    SUCCESS = 2
    FAILED = 3

    description = {
        -1: "暂存",
        1: "作业已提交",
        2: "执行成功",
        3: "执行失败"
    }
