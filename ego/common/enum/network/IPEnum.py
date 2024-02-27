from enum import Enum, unique


@unique
class IPEnum(Enum):
    NONE = "none"
    HOST = "localhost"
    BRIDGE = "bridge"
