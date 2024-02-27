from functools import wraps

from ego import applicationContext

log = applicationContext.log


class TopicSubscriber:
    def __init__(
            self,
            exchange, queue, routing_key,
            exchange_durable=True, exchange_auto_delete=True,
            queue_durable=True, queue_auto_delete=False,
            auto_ack=False,
            prefetch_count=1,
            instance_key="default",
            *args, **kwargs
    ):
        self.ncalls = 0

        self.exchange = exchange
        self.queue = queue
        self.routing_key = routing_key

        self.exchange_durable = exchange_durable
        self.queue_durable = queue_durable
        self.exchange_auto_delete = exchange_auto_delete
        self.queue_auto_delete = queue_auto_delete
        self.auto_ack = auto_ack
        self.prefetch_count = prefetch_count

        self.instance_key = instance_key

    def __call__(self, func):
        self.func = func
        names = self.func.__qualname__.split('.')
        self.clazz_name = self.func.__qualname__.split(".")[0]

        if hasattr(applicationContext, "rabbit_mq_topic_consumers"):
            applicationContext.rabbit_mq_topic_consumers[self.clazz_name][names[1]] = self
        else:
            rabbit_mq_topic_consumers = {
                self.clazz_name: {
                    names[1]: self
                }
            }
            setattr(applicationContext, "rabbit_mq_topic_consumers", rabbit_mq_topic_consumers)

        @wraps(func)
        def wrapper(*args, **kwargs):
            self.ncalls += 1

            return func(*args, **kwargs)

        return wrapper
