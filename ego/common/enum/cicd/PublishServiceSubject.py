from enum import Enum, unique


@unique
class PublishServiceSubject(Enum):
    SERVICE = 0
    INSTANCE = 1

    description = {
        0: "服务发布",
        1: "单实例发布"
    }
