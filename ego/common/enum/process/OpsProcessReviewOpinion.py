from enum import Enum, unique


@unique
class OpsProcessReviewOpinion(Enum):
    """
        审批类型
    """
    PENDING = -1
    PASSED = 1
    REFUSED = 2

    description = {
        -1: "待审批",
        1: "同意",
        2: "驳回",
    }
