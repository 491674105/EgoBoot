from enum import Enum


class OpsCloudHostSpecStatus(Enum):
    # 正常
    NORMAL = "normal"
    # 停用/规格下线
    DEACTIVATE = "deactivate"
    # 售罄
    SELLOUT = "sellout"
    # 公测
    OPEN_BETA = "open_beta"
    # 公测售罄
    OPEN_BETA_SELLOUT = "open_beta_sellout"
    # 推荐(等同normal)
    PROMOTION = "promotion"
