from ego.common.enum.network.HttpMethod import HttpMethod

from ego import applicationContext
from ego.dispatch.feign.FeignMappingDispatch import FeignMapping

log = applicationContext.log


class TaskClientFeign:
    def __init__(self):
        pass

    @FeignMapping(
        service_name="",
        uri="/",
        method=HttpMethod.GET,
        timeout=8
    )
    def start_up_task(self, service_name=None, api_path=None, params=None, data=None, response=None):
        """
            调用远程执行器，启动真实调度逻辑
        """
        log.debug(response)
        if not response:
            log.error("服务器未响应！")
            return False

        if response["code"] != 200 or "data" not in response:
            log.error(response)
            return False

        return True
