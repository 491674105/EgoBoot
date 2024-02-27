from asyncio import sleep as a_sleep
from json import dumps

from werkzeug.exceptions import UnsupportedMediaType

from ego import applicationContext
from ego.logger.service.LoggerCoreService import LoggerCoreService
from ego.common.constant.config import Network
from ego.database_core.transaction.Transaction import Transactional

from ego.dao.LogMapper import LogMapper

log = LoggerCoreService.get_logger_instance()


class LogService:
    logMapper = LogMapper()

    @Transactional()
    async def save_filter_access_log(self, filter_):
        await a_sleep(0.001)

        endpoint = filter_.request.endpoint
        if filter_.request.endpoint not in applicationContext.record_log_endpoints:
            log.debug(f"目标{filter_.request.endpoint}未配置日志切面。")
            return
        log.debug(f"endpoint -> {filter_.request.endpoint}")
        log.debug(applicationContext.record_log_endpoints)
        op_type = applicationContext.record_log_endpoints[filter_.request.endpoint]
        log.debug(f"op_type -> {op_type}")

        if not hasattr(filter_, "host") or filter_.host in (None, ""):
            host = Network.LOCAL_HOST_IP_V4
        else:
            host = filter_.host
        log.debug(host)

        path = filter_.request.path
        log.debug(f"path -> {path}")
        if not hasattr(filter_.g, "user_info") or not filter_.g.user_info:
            log.error(f"主机{host}正在对接口{path}进行非法请求！")
            return
        user_info = filter_.g.user_info
        log.debug(f"groupId -> {user_info.groupId}")

        if not hasattr(user_info, "id") or user_info.id is None:
            log.warning("未知的访问用户！")
            id_ = -1
        else:
            id_ = user_info.id
        log.debug(f"id -> {id_}")

        if not hasattr(user_info, "name") or user_info.name in (None, ""):
            name = "UNKNOWN"
        else:
            name = user_info.name
        log.debug(f"name -> {name}")

        op_log = {
            "uri": path,
            "endpoint": endpoint,
            "table_name": "",
            "op_type": op_type.value,
            "host": host,
            "user_id": id_,
            "operator": name
        }
        log.debug(op_log)
        try:
            pk = self.logMapper.insert_operate_log(op_log)
        except Exception as e:
            log.warning(f"操作日志写入失败，内容：{op_log}")
            log.exception(e)
            return

        try:
            request_body = filter_.request.get_json()
        except UnsupportedMediaType:
            request_body = {}
        log.debug(request_body)
        op_log_detail = {
            "log_id": pk,
            "description": "",
            "detail": dumps(request_body, ensure_ascii=False)
        }
        log.debug(op_log_detail)
        try:
            self.logMapper.insert_operate_log_detail(op_log_detail)
        except Exception as e:
            log.warning(f"操作日志写入失败，内容：{op_log_detail}")
            log.exception(e)
