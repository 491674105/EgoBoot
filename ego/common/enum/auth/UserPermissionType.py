from enum import Enum, unique


@unique
class UserPermissionType(Enum):
    ROOT = "1"
    SYSTEM_OPERATION = "4"
    DATABASE_ADMINISTRATOR = "7"
    SAFETY_ENGINEER = "10"

    description = {
        "1": "超级管理员",
        "4": "系统运维工程师",
        "7": "数据库管理员",
        "10": "安全工程师"
    }

    @staticmethod
    def get_all_roles():
        """
            获取所有管理员（包含安全部门人员）
        """
        role_ids = ["1", "4", "7", "10"]
        roles = []
        for member in UserPermissionType:
            if member.name == "description":
                continue

            if member.value not in role_ids:
                continue
            roles.append(member.value)

        return roles

    @staticmethod
    def get_sys_admin_roles():
        role_ids = ["1", "4"]
        roles = []
        for member in UserPermissionType:
            if member.name == "description":
                continue

            if member.value not in role_ids:
                continue
            roles.append(member.value)
        return roles
