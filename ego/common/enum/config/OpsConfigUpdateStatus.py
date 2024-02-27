from enum import Enum, unique


@unique
class OpsConfigUpdateStatus(Enum):
    """
        服务配置修改计划状态
    """
    INIT = -1
    COMMITTED = 0
    SUCCESS = 1
    FAILED = 2

    description = {
        -1: "初始化",
        0: "作业已提交",
        1: "执行成功",
        2: "执行失败"
    }
