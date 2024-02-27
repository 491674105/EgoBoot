from enum import Enum
from enum import unique


@unique
class OpsVolumeTypeInvalid(Enum):
    description = {}

    """
        华为云废弃/当前无法使用的规格
    """
    HUAWEI_CLOUD = 2

    invalid_specs = {
        2: [
            "DESS_SAS",
            "DESS_SAS_ISCSI",
            "DESS_SAS_FC",
            "DESS_MIX_ISCSI",
            "DESS_MIX_FC",
            "DESS_SSD",
            "DESS_SSD_ISCSI",
            "DESS_SSD_FC",
            "POD1"
        ]
    }
