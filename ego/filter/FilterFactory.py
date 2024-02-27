from ego import applicationContext
from ego.classloader.ClassLoader import ClassLoader

from ego.common.constant.config import Base


class FilterFactory:
    @staticmethod
    def init_filter():
        if "filter_path" not in applicationContext.base_config[getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)]:
            return

        classLoader = ClassLoader(
            applicationContext.base_config[getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)]["filter_path"],
            getattr(applicationContext, Base.MODULE_PATH_KEY)
        )
        filters = classLoader.load()
        setattr(applicationContext, "filters", filters)
