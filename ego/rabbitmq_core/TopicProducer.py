from asyncio import run_coroutine_threadsafe

from functools import wraps
from json import dumps

from aio_pika import Message

from ego import applicationContext
from ego.exception.type.NullPointException import NullPointException

log = applicationContext.log
loop = applicationContext.loop


class TopicProducer:
    def __init__(
            self,
            exchange, queue, routing_key,
            exchange_durable=True, exchange_auto_delete=True,
            queue_durable=True, queue_auto_delete=False,
            prefetch_count=10,
            instance_key="default",
            *args, **kwargs
    ):
        self.ncalls = 0

        self.headers = {}
        self.content_type = "application/json"

        self.exchange = exchange
        self.queue = queue
        self.routing_key = routing_key
        self.exchange_durable = exchange_durable
        self.queue_durable = queue_durable
        self.exchange_auto_delete = exchange_auto_delete
        self.queue_auto_delete = queue_auto_delete
        self.prefetch_count = prefetch_count

        self.topicConnectionPool = getattr(getattr(applicationContext, "rabbit_mq"), instance_key)
        self.channel_info = self.topicConnectionPool

    def __call__(self, func):
        self.func = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            self.ncalls += 1
            log.debug(args)
            log.debug(kwargs)

            if len(args) == 1 and not kwargs:
                log.error("参数丢失！")
                return

            if "msg" not in kwargs:
                log.error("缺少必要参数【msg】")
                raise NullPointException("缺少必要参数【msg】")
            log.debug(kwargs["msg"])
            msg = kwargs["msg"]
            future = run_coroutine_threadsafe(self.__send(msg), loop)
            log.debug(future)
            log.debug(future.result())
            kwargs["result"] = future.result()

            return func(*args, **kwargs)

        return wrapper

    async def __send(self, msg):
        log.debug(msg)
        if type(msg) == dict:
            real_msg = dumps(msg)
        elif type(msg) == list:
            real_msg = ' '.join(msg)
        else:
            real_msg = msg
        if self.headers:
            message = Message(real_msg.encode("UTF-8"), content_type=self.content_type, headers=self.headers)
        else:
            message = Message(real_msg.encode("UTF-8"), content_type=self.content_type)
        log.debug(message)

        async with self.topicConnectionPool.channel_pool.acquire() as channel:
            try:
                if channel.is_closed:
                    await channel.reopen()
                exchange_inst = await channel.declare_exchange(
                    name=self.exchange,
                    type="topic",
                    durable=self.exchange_durable,
                    auto_delete=self.exchange_auto_delete
                )
                queue_inst = await channel.declare_queue(
                    name=self.queue,
                    durable=self.queue_durable,
                    auto_delete=self.queue_auto_delete
                )
                await queue_inst.bind(exchange=self.exchange, routing_key=self.routing_key)
                await exchange_inst.publish(
                    routing_key=self.routing_key,
                    message=message
                )
                return True
            except Exception as e:
                log.exception(e)
                return False

    async def send_body(self, msg):
        await self.__send(msg)
