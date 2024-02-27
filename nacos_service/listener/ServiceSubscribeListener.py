from ego import routeContainer, applicationContext

from ego.common.constant.config import Network

from ego.exception.type.UnresolvedException import UnresolvedException


class ServiceSubscribeListener:
    """
        Nacos服务监听器
    """

    def __init__(self, nacos_client, service_list, ttl=None):
        self.nacos_client = nacos_client
        self.service_list = service_list
        self.ttl = 60
        if ttl:
            self.ttl = ttl

    def load_static_instance(self):
        """
            静态主机信息
        """
        for service in self.service_list:
            if not service or "static" not in service:
                continue

            service_name = service["name"]
            static_info = service["static"]
            if isinstance(static_info, dict):
                routeContainer.add_instance(
                    service_name=service_name,
                    ip=static_info["ip"],
                    port=static_info["port"]
                )
                continue

            if isinstance(static_info, list):
                for static in static_info:
                    routeContainer.add_instance(
                        service_name=service_name,
                        ip=static["ip"],
                        port=static["port"]
                    )
            raise UnresolvedException("静态订阅信息配置异常！")

    def apply_instance_info(self):
        """
            动态主机信息
        """
        for service in self.service_list:
            if not service or "static" in service:
                continue

            service_name = service["name"]
            service_info = self.nacos_client.list_naming_instance(
                service_name=service_name
            )
            for host in service_info["hosts"]:
                routeContainer.add_instance(
                    service_name=service_name,
                    ip=host["ip"],
                    port=host["port"]
                )
        setattr(applicationContext, Network.SUBSCRIBE_FLAG, True)
