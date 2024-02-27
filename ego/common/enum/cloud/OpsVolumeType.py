from enum import Enum
from enum import unique


@unique
class OpsVolumeType(Enum):
    description = {}

    """
        华为云规格描述
    """
    # 常规云硬盘规格
    SATA = "SATA"
    SAS = "SAS"
    CO_P1 = "co-p1"
    GPSSD = "GPSSD"
    UH_L1 = "uh-l1"
    SSD = "SSD"
    GPSSD2 = "GPSSD2"
    ESSD = "ESSD"
    ESSD2 = "ESSD2"

    description["SATA"] = "普通IO（上一代产品）"
    description["SAS"] = "高IO"
    description["co-p1"] = "高IO (性能优化Ⅰ型)"
    description["GPSSD"] = "通用型SSD"
    description["uh-l1"] = "超高IO(时延优化)"
    description["SSD"] = "超高IO"
    description["GPSSD2"] = "通用型SSD V2"
    description["ESSD"] = "极速型SSD"
    description["ESSD2"] = "极速型SSD V2"

    # 专属云裸金属服务器硬盘规格
    DESS_SAS = "DESS_SAS"
    DESS_SAS_ISCSI = "DESS_SAS_ISCSI"
    DESS_SAS_FC = "DESS_SAS_FC"
    DESS_MIX_ISCSI = "DESS_MIX_ISCSI"
    DESS_MIX_FC = "DESS_MIX_FC"
    DESS_SSD = "DESS_SSD"
    DESS_SSD_ISCSI = "DESS_SSD_ISCSI"
    DESS_SSD_FC = "DESS_SSD_FC"

    description["DESS_SAS"] = "普通I/O企业存储"
    description["DESS_SAS_ISCSI"] = "普通I/O企业存储"
    description["DESS_SAS_FC"] = "普通I/O企业存储"
    description["DESS_MIX_ISCSI"] = "高I/O企业存储"
    description["DESS_MIX_FC"] = "高I/O企业存储（低延时）"
    description["DESS_SSD"] = "超高I/O企业存储"
    description["DESS_SSD_ISCSI"] = "超高I/O企业存储"
    description["DESS_SSD_FC"] = "超高I/O企业存储（低延时）"

    # 废弃规格
    POD1 = "POD1"
    description["POD1"] = "废弃规格"
