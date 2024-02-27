from enum import Enum


class OpsProcessClaimStatus(Enum):
    # 研发录入发布信息
    P1 = "p2"
    # 测试工程师验收
    P9 = "p10"
    # 产品经理验收
    P10 = "p11"
    # 项目经理验收
    P11 = "p12"

    status_dict = {
        "p2": 2,
        "p10": 4,
        "p11": 4,
        "p12": 4
    }
