
class RedisUserDTO:
    # 登录会话token
    token = None
    # 用户ID
    id = None
    # 微信用户唯一ID
    wxUserId = None
    # 用户名
    name = None
    # 微信头像
    avatar = None
    # 用户邮箱
    email = None
    # 用户组：1 ---> 超级管理员  2 ---> 为普通用户
    groupId = None
    # 岗位
    userPosition = None
    # 员工编号
    employeeNumber = None
