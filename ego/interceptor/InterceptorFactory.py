from ego import applicationContext
from ego.classloader.ClassLoader import ClassLoader

from ego.common.constant.config import Base


class InterceptorFactory:
    @staticmethod
    def init_interceptor():
        if "interceptor_path" not in applicationContext.base_config[getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)]:
            return

        classLoader = ClassLoader(
            applicationContext.base_config[getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)]["interceptor_path"],
            getattr(applicationContext, Base.MODULE_PATH_KEY)
        )
        interceptors = classLoader.load()
        setattr(applicationContext, "interceptors", interceptors)
