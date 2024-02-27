from typing import Union

from redis import ConnectionPool, Redis

from ego.redis_core.client.Client import Client
from ego.common.enum.redis.RedisType import RedisType


class RedisStore:
    def __init__(self):
        pass


class RedisClient(Client):
    __attr_names = {
        "host", "port", "mode", "db", "password", "ssl", "ssl_ca_certs", "ssl_cert_reqs"
    }

    def __init__(self, host=None, port=None, mode=RedisType.SINGLE, **kwargs):
        super(RedisClient, self).__init__()
        if host:
            self.host: Union[str, None] = host
        if port:
            self.port: Union[str, None] = port
        if mode:
            self.mode: RedisType = mode

        self.db: int = 0
        if "db" in kwargs:
            self.db = kwargs["db"]

        self.password: str = ""
        if "password" in kwargs:
            self.password = kwargs["password"]

        self.ssl: bool = False
        self.ssl_ca_certs: Union[str, None] = ...
        self.ssl_cert_reqs: Union[str, None] = ...
        if "ssl" in kwargs:
            self.ssl = kwargs["ssl"]
            self.ssl_ca_certs = kwargs["ssl_ca_certs"]
            self.ssl_cert_reqs = kwargs["ssl_cert_reqs"]

        self.client: Union[Redis, None] = ...

    def update(self, configs):
        for k in configs:
            if k != "mode":
                setattr(self, k, configs[k])
                continue
            setattr(self, k, RedisType.get_type_by_code(configs[k]))

    def init(self):
        if self.mode == RedisType.SINGLE:
            self.__create_single_point_client()
            return

        if self.mode == RedisType.CLUSTER:
            return

        if self.mode == RedisType.SENTINEL:
            return

    def __create_single_point_client(self):
        if not self.ssl:
            pool = ConnectionPool(
                host=self.host, port=self.port,
                db=self.db,
                password=self.password
            )
        else:
            pool = ConnectionPool(
                host=self.host, port=self.port,
                db=self.db,
                password=self.password,
                ssl=self.ssl, ssl_ca_certs=self.ssl_ca_certs, ssl_cert_reqs=self.ssl_cert_reqs
            )
        self.client = Redis(connection_pool=pool)

    def __create_cluster_client(self):
        raise NotImplementedError("coming soon...")

    def __create_sentinel_client(self):
        raise NotImplementedError("coming soon...")

    def set(self, key, value, **kwargs):
        """
            创建key并赋值value
            ex：设置一个秒级超时
            px：设置一个毫秒级超时
            nx：键不存在的时候设置键值，默认False
            xx：键存在的时候设置键值，默认False
            keepttl：保留指定键上一次设定的生存时间（Redis 6.0以后加入的功能）
            get：返回指定键原本的值，若键不存在时返回None(Redis 6.2以后加入的功能)
            exat：设置以秒为单位的UNIX时间戳所对应的时间为过期时间
            pxat：设置以毫秒为单位的UNIX时间戳所对应的时间为过期时间
        """
        return self.client.set(name=key, value=value, **kwargs)

    def setnx(self, key, value, **kwargs):
        return self.set(key=key, value=value, nx=True, **kwargs)

    def hset(self, hash_name, key, value, **kwargs):
        """
            使用Hash表保存key/value
            hash_name：需要保存的hash值/未进行hash操作的字符串
            key：保存的键
            value：保存的值
            mapping：需要直接存储多个不同key/value时传入
            items：需要将多个key与同一value保存时传入
        """
        return self.client.hset(name=hash_name, key=key, value=value, **kwargs)

    def get(self, key):
        return self.client.get(key)

    def hget(self, hash_name, key):
        return self.client.hget(name=hash_name, key=key)

    def keys(self, pattern, **kwargs):
        return self.client.keys(pattern, **kwargs)

    def ttl(self, key):
        return self.client.ttl(key)

    def type(self, key):
        return self.client.type(key)

    def delete(self, key):
        return self.client.delete(key)

    def execute_command(self, *args, **options):
        """
            For example::
             self.execute_command("GET", name)
        """
        return self.client.execute_command(*args, **options)
