from enum import Enum, unique


@unique
class CMDBProjectRelativeType(Enum):
    # 与系统/项目的关系
    RELATION_WITH_PROJECT = 1
    # 与服务的关系
    RELATION_WITH_SERVICE = 2
    # 与实例的关系
    RELATION_WITH_INSTANCE = 3
