from asyncio import run_coroutine_threadsafe

from ego import applicationContext

log = applicationContext.log
loop = applicationContext.loop


class RabbitMQTopic:
    def __init__(
            self,
            *args, **kwargs
    ):
        self.ncalls = 0

    def __call__(self, clazz):
        self.clazz = clazz
        self.inst = self.clazz()
        clazz_name = self.clazz.__name__
        if hasattr(applicationContext, "rabbit_mq_topic_consumers") \
                and clazz_name in applicationContext.rabbit_mq_topic_consumers:
            self.rabbit_mq_topic_consumers = applicationContext.rabbit_mq_topic_consumers[clazz_name].copy()

            for consumer_name in self.rabbit_mq_topic_consumers:
                consumer = self.rabbit_mq_topic_consumers[consumer_name]
                func = getattr(self.inst, consumer_name)

                run_coroutine_threadsafe(self.__bind(callback=func, consumer_properties=consumer), loop)
                if clazz_name not in applicationContext.rabbit_mq_topic_consumers:
                    continue
                if consumer_name not in applicationContext.rabbit_mq_topic_consumers[clazz_name]:
                    continue
                del applicationContext.rabbit_mq_topic_consumers[clazz_name][consumer_name]

        return clazz

    @staticmethod
    async def __bind(callback, consumer_properties):
        topicConnectionPool = getattr(
            getattr(applicationContext, "rabbit_mq"),
            consumer_properties.instance_key
        )

        async with topicConnectionPool.channel_pool.acquire() as channel:
            if channel.is_closed:
                await channel.reopen()
            await channel.set_qos(prefetch_count=consumer_properties.prefetch_count)
            await channel.declare_exchange(
                name=consumer_properties.exchange,
                type="topic",
                durable=consumer_properties.exchange_durable,
                auto_delete=consumer_properties.exchange_auto_delete
            )
            queue_inst = await channel.declare_queue(
                name=consumer_properties.queue,
                durable=consumer_properties.queue_durable,
                auto_delete=consumer_properties.queue_auto_delete
            )
            await queue_inst.bind(exchange=consumer_properties.exchange, routing_key=consumer_properties.routing_key)
            await queue_inst.consume(callback)
