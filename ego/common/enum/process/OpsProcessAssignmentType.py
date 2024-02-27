from enum import Enum, unique


@unique
class OpsProcessAssignmentType(Enum):
    """
        流程归属类型
    """
    CREATE_BY_ME = 1
    REVIEW_BY_ME = 2
    ARCHIVED = 3
    PASS_ME = 4

    description = {
        1: "由我创建",
        2: "由我办理",
        3: "已归档（与我相关）",
        4: "在途（与我相关）"
    }
