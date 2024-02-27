from enum import Enum, unique


@unique
class ServiceType(Enum):
    """
        服务类型
    """
    # WEBSITE = "website"
    # JAR = "jar"
    BIGDATA = "bigdata"
    Front = "Front"
    BackEnd = "Backend"

    description = {
        # "website": "WEB前端",
        # "jar": "JAVA后端",
        "bigdata": "大数据服务",
        "Front": "前端服务",
        "Backend": "后端服务"
    }
