import logging

from threading import Lock

from aio_pika import logger
from aio_pika import connect_robust
from aio_pika.pool import Pool


class TopicConnectionPool:
    __connection_key_prefix = "top.connection"

    __lock = Lock()

    def __init__(
            self,
            loop,
            host=None, port=None,
            username=None, password=None,
            vhost=None,
            max_connection_size=5, max_channel_size=10,
            *args, **kwargs
    ):
        """
            host: MQ服务地址
            port: MQ服务端口
            username: 登录用户，默认None
            password: 密码，默认None
            vhost: 虚拟主机名/命名空间
            max_connection_size: 连接池最大连接数
            max_channel_size：每个连接可申请得最大管道数
        """
        self.loop = loop
        self.host = None
        if host:
            self.host = host
        self.port = None
        if port:
            self.port = port

        self.auth_flag = False
        self.username = None
        if username:
            self.auth_flag = True
            self.username = username
        self.password = None
        if password:
            self.password = password
        self.vhost = None
        if vhost:
            self.vhost = vhost

        self.max_connection_size = max_connection_size
        self.max_channel_size = max_channel_size
        self.connection_pool = None
        self.channel_pool = None

        if "log" in kwargs:
            self.log = kwargs["log"]
        else:
            logger.setLevel(logging.ERROR)
            self.log = logger

    async def create_connection(self):
        connection = None
        try:
            connection = await connect_robust(
                host=self.host,
                port=self.port,
                login=self.username,
                password=self.password,
                virtualhost=self.vhost
            )
        except Exception as e:
            self.log.exception(e)
        return connection

    async def create_channel(self):
        async with self.connection_pool.acquire() as connection:
            return await connection.channel()

    def create_pool(self):
        self.connection_pool = Pool(self.create_connection, max_size=self.max_connection_size, loop=self.loop)
        self.channel_pool = Pool(self.create_channel, max_size=self.max_channel_size, loop=self.loop)
