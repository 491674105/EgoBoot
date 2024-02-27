from enum import Enum, unique


@unique
class OpType(Enum):
    NORMAL = 1
    INSERT = 2
    UPDATE = 3
    DELETE = 4
