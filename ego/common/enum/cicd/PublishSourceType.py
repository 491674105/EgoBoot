from enum import Enum, unique


@unique
class PublishSourceType(Enum):
    DEFAULT = -1
    # SQL = 1
    CMDB = 2
    WORKFLOW = 3
    # CONFCENTER = 4

    description = {
        -1: "",
        1: "数据库管理",
        2: "CMDB",
        3: "工单管理服务",
        4: "配置管理服务"
    }
