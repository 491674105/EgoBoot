from enum import Enum


class OpsVolumeTypeOrder(Enum):
    # 默认排序
    DEFAULT = -1

    # 常规云硬盘规格
    SATA = 1
    SAS = 2
    CO_P1 = 2
    GPSSD = 3
    UH_L1 = 4
    SSD = 4
    GPSSD2 = 5
    ESSD = 6
    ESSD2 = 7

    # 专属云裸金属服务器硬盘规格
    DESS_SAS = 1
    DESS_SAS_ISCSI = 1
    DESS_SAS_FC = 2
    DESS_MIX_ISCSI = 3
    DESS_MIX_FC = 4
    DESS_SSD = 5
    DESS_SSD_ISCSI = 5
    DESS_SSD_FC = 6

    # 废弃规格
    POD1 = 10
