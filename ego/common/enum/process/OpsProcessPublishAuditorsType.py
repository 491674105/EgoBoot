from enum import Enum, unique


@unique
class OpsProcessPublishAuditorsType(Enum):
    """
        发布流程关联人员类型
    """
    TEST_ENGINEER = 1
    DEVELOPMENT_ENGINEER = 2

    description = {
        1: "测试工程师",
        2: "开发工程师"
    }
