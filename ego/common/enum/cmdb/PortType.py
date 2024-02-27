from enum import Enum, unique


@unique
class PortType(Enum):
    SPECIAL = 0
    BUSINESS = 1
    RANDOM = 2

    description = {
        0: "专用端口",
        1: "业务端口",
        2: "随机端口",
    }
