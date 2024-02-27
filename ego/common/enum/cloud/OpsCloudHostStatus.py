from enum import Enum


class OpsCloudHostStatus(Enum):
    # 创建实例后，在实例状态进入运行中之前的状态
    BUILD = "build"
    # 实例正在进行重启操作
    REBOOT = "reboot"
    # 实例正在进行强制重启操作
    HARD_REBOOT = "hard_reboot"
    # 实例正在重建中
    REBUILD = "rebuild"
    # 实例正在热迁移中
    MIGRATING = "migrating"
    # 实例接收变更请求，开始进行变更操作
    RESIZE = "resize"
    # 实例正常运行状态
    ACTIVE = "active"
    # 实例被正常停止
    SHUTDOWN = "shutdown"
    # 实例正在回退变更规格的配置
    REVERT_RESIZE = "revert_resize"
    # 实例正在校验变更完成后的配置
    VERIFY_RESIZE = "verify_resize"
    # 实例处于异常状态
    ERROR = "error"
    # 实例已被正常删除
    DELETED = "deleted"
    # 镜像启动的实例处于搁置状态
    SHELVED = "shelved"
    # 卷启动的实例处于搁置状态
    SHELVED_OFFLOADED = "shelved_offloaded"
    # 实例处于未知状态
    UNKNOWN = "unknown"

    description = {
        "build": "实例已创建",
        "reboot": "正在重启",
        "hard_reboot": "正在强制重启",
        "rebuild": "实例重建中",
        "migrating": "正在热迁移实例",
        "resize": "正在进行实例变更",
        "active": "正常运行",
        "shutdown": "停止",
        "revert_resize": "正在回退实例变更",
        "verify_resize": "变更校验中",
        "error": "实例异常",
        "deleted": "实例已删除",
        "shelved": "镜像启动搁置",
        "shelved_offloaded": "卷启动搁置",
        "unknown": "未知"
    }
