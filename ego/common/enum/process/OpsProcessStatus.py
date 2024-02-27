from enum import Enum, unique


@unique
class OpsProcessStatus(Enum):
    """
        流程状态
    """
    NO_STATUS = -2
    CACHE = -1
    CREATE = 1
    INITIATE = 2
    MOVING = 3
    TO_SIGN = 4
    REVIEWING = 5
    TO_HANDLE = 6
    IN_HAND = 7
    HANDLED = 8
    REFUSE = 9
    SEND_BACK = 10
    INVALID = 11
    ARCHIVED = 12

    description = {
        -2: "无状态",
        -1: "缓存",
        1: "新建",
        2: "初始化",
        3: "流转",
        4: "待签收",
        5: "审批中",
        6: "待处理",
        7: "处理中",
        8: "已处理",
        9: "拒收",
        10: "退回",
        11: "作废",
        12: "归档",
    }
