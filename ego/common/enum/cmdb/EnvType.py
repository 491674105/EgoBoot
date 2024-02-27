from enum import Enum, unique


@unique
class EnvType(Enum):
    OFFLINE = 1
    ONLINE = 2

    description = {
        1: "线下环境",
        2: "线上环境"
    }
