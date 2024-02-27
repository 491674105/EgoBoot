from enum import Enum
from enum import unique


@unique
class TriggerType(Enum):
    CRON = "cron"
    DATE = "date"
    DATETIME = "datetime"
    INTERVAL = "interval"
