from enum import Enum, unique


@unique
class PublishServiceType(Enum):
    UPDATE = "update"
    MOVE = "move"
    ROLLBACK = "rollback"

    NOT_MATCH = "not_match"

    @staticmethod
    def get_type_by_name(name):
        for member in PublishServiceType:
            if member.value == name:
                return member

        return PublishServiceType.NOT_MATCH

    @staticmethod
    def get_desc(value):
        if value == "service":
            return {
                "update": "更新发布",
                "rollback": "回滚发布"
            }

        return {
            "move": "迁移发布"
        }

    description = {
        "update": "更新发布",
        "move": "迁移发布",
        "rollback": "回滚发布"
    }
