class NacosRegister:
    __default_reporting_interval = 5

    def __init__(self, ip, port, service_name, nacos_client, nacos_config):
        self.nacos_client = nacos_client
        self.nacos_config = nacos_config

        self.service_config = nacos_config["nacos"]

        self.ip = ip

        self.service_name = service_name
        self.port = port
        self.cluster_name = self.service_config["cluster_name"]
        if "reporting_interval" in self.service_config:
            self.reporting_interval = self.service_config["reporting_interval"]
        else:
            self.reporting_interval = self.__default_reporting_interval

    def register(self, metadata):
        """
            服务注册
        """
        self.nacos_client.add_naming_instance(
            service_name=self.service_name,
            ip=self.ip,
            port=self.port,
            cluster_name=self.cluster_name,
            metadata=metadata
        )

    def report_beat(self, metadata):
        """
            心跳发送
        """
        self.nacos_client.send_heartbeat(
            service_name=self.service_name,
            ip=self.ip,
            port=self.port,
            cluster_name=self.cluster_name,
            metadata=metadata
        )
