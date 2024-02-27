from enum import Enum, unique


@unique
class CiCdError(Enum):
    BUILD = 1
    PULLCODE = 2
    MIDDLEWARE = 3
    WEIGHT = 4
    UPDATE = 5
    CLEANWORKSPACE = 6
    MOVE = 7
    CDN = 8
    ENVIRONMENT = 9
    FRONTPROJECT = 10
    NODES = 11
    CMD = 12
    REMOTE = 13
    PARAMS = 14
    CHECKROLLBACKTAG = 15
    STOPOLDNODE = 16
    DELETEOLDNODECONF = 17
    RELOADAFTERMOVE = 18


    description = {
        1: "代码BUILD失败",
        2: "拉取代码失败",
        3: "中间件检测失败",
        4: "流量切换失败",
        5: "代码或配置更新失败",
        6: "workspace清理失败",
        7: "代码或配置迁移失败",
        8: "CDN推送失败",
        9: "环境检测失败",
        10: "查询前端项目失败",
        11: "查询前端项目所在节点失败",
        12: "获取Windows命令失败",
        13: "获取远程文件失败",
        14: "传入必要参数有缺失",
        15: "回滚TAG检查失败",
        16: "下线旧服务节点实例",
        17: "下线就服务节点配置",
        18: "重新加载supervisor配置"
    }
