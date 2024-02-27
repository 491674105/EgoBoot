from enum import Enum, unique


@unique
class PublishServiceStatus(Enum):
    SUCCESS = 1
    FAILED = 2
    RUNNING = 3
    UNKNOWN = -1
    COMMIT_FAILED = -2

    description = {
        -1: "作业已提交",
        -2: "作业提交异常",
        1: "发布完成",
        2: "发布失败",
        3: "作业执行中",
    }
