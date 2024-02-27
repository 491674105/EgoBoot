from asyncio import run_coroutine_threadsafe
from asyncio import sleep as a_sleep
from time import sleep

from redis import Redis

from ego import applicationContext, ApplicationContext
from ego.logger.service.LoggerCoreService import LoggerCoreService
from ego.coroutine.service.LoopCoreService import LoopCoreService
from ego.redis_core.client.default.RedisClient import RedisClient
from ego.listener.Event import Event
from ego.listener.Listener import Listener
from ego.listener.ListenerManager import ListenerManager

from ego.common.constant.config import Base

from ego.exception.type.NullPointException import NullPointException


class RedisCoreService:
    def __call__(self, clazz):
        if "redis" not in applicationContext.base_config[getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)]:
            return clazz

        self.log = LoggerCoreService.get_logger_instance()

        RedisCoreService.connect()

        run_coroutine_threadsafe(self.register_listen(), LoopCoreService.get_loop_instance())
        return clazz

    async def register_listen(self):
        while not hasattr(applicationContext, Base.DEFAULT_APP_LAUNCHED_KEY) \
                or not getattr(applicationContext, Base.DEFAULT_APP_LAUNCHED_KEY):
            await a_sleep(1)

        while ListenerManager.LAZY_LOAD_KEY not in applicationContext.lazy_module_launched \
                or not applicationContext.lazy_module_launched[ListenerManager.LAZY_LOAD_KEY]:
            await a_sleep(1)

        event = Event()
        event.handler_ = self.keepalive
        event.kwargs_ = {"redis_config": applicationContext.base_config[
            getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)
        ]["redis"]}
        listener = Listener()
        listener.event_ = event
        listener.listener_interval = 60
        applicationContext.listener_manager.register(listener)

    @staticmethod
    def keepalive(redis_config):
        if not hasattr(applicationContext, "redis") or not getattr(applicationContext, "redis"):
            redis_client_context = ApplicationContext()
            setattr(applicationContext, "redis", redis_client_context)
        else:
            redis_client_context = getattr(applicationContext, "redis")

        for attr in redis_config:
            if hasattr(redis_client_context, attr["name"]) and getattr(redis_client_context, attr["name"]):
                continue

            redis_client = RedisClient()
            redis_client.update(attr)
            redis_client.init()
            setattr(redis_client_context, attr["name"], redis_client)

    @staticmethod
    def connect():
        redis_client_context = ApplicationContext()
        setattr(applicationContext, "redis", redis_client_context)
        for attr in applicationContext.base_config[getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)]["redis"]:
            redis_client = RedisClient()
            redis_client.update(attr)
            redis_client.init()
            setattr(redis_client_context, attr["name"], redis_client)

    @staticmethod
    def get_redis_instance(key=None) -> RedisClient:
        if not applicationContext:
            raise NullPointException("ApplicationContext is empty.")

        if not hasattr(applicationContext, "redis") or not getattr(applicationContext, "redis"):
            raise NullPointException("can not find the redis instance.")

        redis_instances = getattr(applicationContext, "redis")
        if not key or key == "":
            inst_name = "redis_main"
        else:
            inst_name = key

        if not hasattr(redis_instances, inst_name):
            sleep(10)
            if not hasattr(redis_instances, inst_name):
                RedisCoreService.connect()
        return getattr(redis_instances, inst_name)

    @staticmethod
    def get_redis_real_instance(key=None) -> Redis:
        redis_instance = RedisCoreService.get_redis_instance(key=key)

        return getattr(redis_instance, "client")
