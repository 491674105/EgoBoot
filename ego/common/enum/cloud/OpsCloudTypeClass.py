from enum import Enum
from enum import unique


@unique
class OpsCloudTypeClass(Enum):
    """
        云上状态/类型分类
    """
    # 计费场景
    CHARGE_SCENE = "charge_scene"
    # 计费类型
    CHARGE_MODE = "charge_mode"
    # 周期类型
    PERIOD_TYPE = "period_type"
    # 云主机规格状态
    HOST_SPEC_STATUS = "host_spec_status"
    # 云镜像状态
    IMAGE_STATUS = "image_status"
    # 云主机状态
    HOST_STATUS = "host_status"
    # 金额计量单位
    UNIT_CODE = "unit_code"
    # 云订单来源
    ORDER_SOURCE_TYPE = "order_source_type"
    # 云订单状态
    ORDER_STATUS = "order_status"
    # 云订单类型
    ORDER_TYPE = "order_type"
    # 订单折扣类型
    ORDER_DISCOUNT_TYPE = "order_discount_type"
    # 账单类型
    BILL_TYPE = "bill_type"
