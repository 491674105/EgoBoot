from enum import Enum
from enum import unique


@unique
class SchedulerType(Enum):
    INLINE = 1
    OUTLINE = 2
