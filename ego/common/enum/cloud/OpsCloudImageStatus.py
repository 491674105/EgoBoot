from enum import Enum


class OpsCloudImageStatus(Enum):
    # 表示镜像元数据已经创建成功，等待上传镜像文件
    INIT = 'init'
    # 表示镜像正在上传文件到后端存储
    UPLOAD = 'upload'
    # 表示镜像已经删除
    DELETED = 'deleted'
    # 表示镜像上传错误
    ERROR = 'error'
    # 表示镜像可以正常使用
    ACTIVE = 'active'
