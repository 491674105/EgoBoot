from ego import applicationContext, ApplicationContext
from ego.common.constant.config import Base

from ego.rabbitmq_core.connection.TopicConnectionPool import TopicConnectionPool


class RabbitMQService:
    def __call__(self, clazz):
        if "rabbitmq" not in applicationContext.base_config[getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)]:
            return clazz

        rabbit_mq_context = ApplicationContext()
        setattr(applicationContext, "rabbit_mq", rabbit_mq_context)
        rabbitmq_configs = applicationContext.base_config[getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)]["rabbitmq"]
        if isinstance(rabbitmq_configs, dict):
            topicConnectionPool = TopicConnectionPool(
                **rabbitmq_configs,
                log=applicationContext.log,
                loop=applicationContext.loop
            )
            topicConnectionPool.create_pool()
            setattr(rabbit_mq_context, "default", topicConnectionPool)
        else:
            pass

        return clazz
