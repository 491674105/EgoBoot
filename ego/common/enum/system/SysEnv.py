from enum import Enum, unique


@unique
class SysEnv(Enum):
    # 托管
    HOSTING_OPEN = "hosting_open"
    HOSTING_CLOSE = "hosting_close"
    # 开发者模式
    RUNNING_MODE_DEVELOPER = "developer"
    # 服务器模式
    RUNNING_MODE_SERVER = "server"
