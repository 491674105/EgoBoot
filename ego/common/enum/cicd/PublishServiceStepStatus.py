from enum import Enum, unique


@unique
class PublishServiceStepStatus(Enum):
    ERROR = -1
    START_UP = 0
    RUNNING = 1
    FINISH = 2

    description = {
        -1: "执行异常",
        0: "开始执行",
        1: "执行中",
        2: "执行完成",
    }
