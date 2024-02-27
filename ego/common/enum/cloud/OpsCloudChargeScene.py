from enum import Enum
from enum import unique


@unique
class OpsCloudChargeScene(Enum):
    ALL = "all"
    PERIOD = "period"
    DEMAND = "demand"
