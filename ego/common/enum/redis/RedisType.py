from enum import Enum, unique


@unique
class RedisType(Enum):
    SINGLE = 0
    CLUSTER = 1
    SENTINEL = 2

    @staticmethod
    def get_type_by_code(code):
        for member in RedisType:
            if member.value == code:
                return member

        return RedisType.SINGLE

    @staticmethod
    def get_desc(code):
        if code == 0:
            return "single_point"
        if code == 1:
            return "cluster"
        if code == 2:
            return "sentinel"
