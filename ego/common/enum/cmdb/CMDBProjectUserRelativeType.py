from enum import Enum, unique


@unique
class CMDBProjectUserRelativeType(Enum):
    """
        用户信息绑定类型（1：角色信息绑定 2：用户信息绑定）
    """
    RELATION_WITH_ROLE = 1
    RELATION_WITH_USER = 2
