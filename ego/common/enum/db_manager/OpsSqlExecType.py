from enum import Enum, unique


@unique
class OpsSqlExecType(Enum):
    """
        SQL执行计划类型
    """
    NORMAL = 1
    before_publish = 2
    after_publish = 3

    description = {
        1: "跟随发布计划执行",
        2: "服务发布前执行",
        3: "服务发布后执行"
    }
