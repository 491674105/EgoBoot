from enum import Enum, unique


@unique
class NoticeEnum(Enum):
    """
        通知类型
    """
    DEVELOP = 1
    SIGN = 2
    DEVELPRESULT = 3
    AFTERSQL = 4
    FAILED = 5
    FINISH = 6
    PUSHFAILED = 7
    PUSHALERT = 8
    ISRECOVERY = 9

    description = {
        1: {
            "content": f"### 工单-待处理通知\n"
        },
        2: {
            "content": f"### 工单-待签收通知\n"
        },
        3: {
            "content": f"### 工单-发布结果通知\n"
        },
        4: {
            "content": f"### 工单-SQL执行失败通知\n"
        },
        5: {
            "content": f"### 工单-发布失败通知\n"
        },
        6: {
            "content": f"### 工单-归档通知\n"
        },
        7: {
            "content": f"### SQL脚本推送失败通知\n"
        },
        8: {
            "content": "<font color=\"warning\">告警！！！请相关同事注意</font> \n"
        },
        9: {
            "content": f"<font color=\"info\"> 故障恢复</font> \n"
        }

    }
