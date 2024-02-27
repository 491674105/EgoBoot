from enum import Enum, unique


@unique
class CiCdRequireParams(Enum):
    APP_TYPE = "服务类型"
    APP_METHOD = "发布方式"
    APP_ENV = "发布环境"
    APP_NAME = "服务名"
    APP_ZONE = "ZONE"
    GIT_TAG = "tag或分支"
