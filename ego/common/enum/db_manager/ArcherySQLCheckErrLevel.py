from enum import Enum, unique


@unique
class ArcherySQLCheckErrLevel(Enum):
    WARNING = 1
    ERROR = 2

    description = {
        1: "SQL检查警告",
        2: "SQL检查错误"
    }
