from nacos import NacosClient
from yaml import safe_load

from ego import applicationContext

from ego.common.constant.config import Base, Ego, Flask
from nacos_service.base import settings

from ego.exception.type.NullPointException import NullPointException

from ego.flask_core.config.FlaskConfig import FlaskConfig
from ego.utils.file.ConfigHandler import ConfigHandler


class NacosFlaskConfig(FlaskConfig):
    def __init__(self, *args, **kwargs):
        super(NacosFlaskConfig, self).__init__(*args, **kwargs)
        self.nacos_client = None
        self.nacos_cloud_config = None

    def __call__(self, clazz):
        self.clazz = clazz

        self.load_base_config()

        # 获取nacos配置内容
        if Ego.DEFAULT_EGO_CONFIG_KEY in self.base_config and "cloud" in self.base_config[Ego.DEFAULT_EGO_CONFIG_KEY]:
            cloud_config = self.query_config(self.base_config[Ego.DEFAULT_EGO_CONFIG_KEY]["cloud"]["nacos"]["config"])
            config_key = Ego.DEFAULT_EGO_CONFIG_KEY
        elif Flask.DEFAULT_FLASK_CONFIG_KEY in self.base_config \
                and "cloud" in self.base_config[Flask.DEFAULT_FLASK_CONFIG_KEY]:
            cloud_config = self.query_config(
                self.base_config[Flask.DEFAULT_FLASK_CONFIG_KEY]["cloud"]["nacos"]["config"]
            )
            config_key = Flask.DEFAULT_FLASK_CONFIG_KEY
        else:
            raise NullPointException("unknown cloud config.")

        setattr(applicationContext, Base.BASE_CONFIG_VALID_KEY, config_key)

        # 将nacos配置载入本地
        self.merge_config(cloud_config)

        # 配置日志全局日志级别
        self.set_log_level()

        if Ego.DEFAULT_EGO_CONFIG_KEY in self.base_config:
            self.update_ego_config()
        self.update_flask_config()

        self.set_env()
        setattr(applicationContext, "nacos_config", self.base_config[config_key]["cloud"])
        # 缓存静态订阅
        self.cache_static_subscription()

        return clazz

    def query_config(self, data_id):
        self.nacos_client = NacosClient(
            settings.SERVER_ADDRESSES,
            namespace=settings.DEFAULT_NAMESPACES[settings.ENVIRONMENT[self.env]]
        )
        setattr(applicationContext, "nacos_client", self.nacos_client)
        return safe_load(self.nacos_client.get_config(data_id, settings.GROUP))

    def merge_config(self, cloud_config):
        b_handler = ConfigHandler()
        b_handler.set_source_json(self.base_config.copy())
        b_handler.iteration()
        base_config_cache = b_handler.get_dist()

        n_handler = ConfigHandler()
        n_handler.set_source_json(cloud_config.copy())
        n_handler.iteration()
        nacos_config_cache = n_handler.get_dist()

        merge_dict = {}
        merge_dict.update(nacos_config_cache)
        merge_dict.update(base_config_cache)

        r_handler = ConfigHandler()
        r_handler.set_source_json(merge_dict.copy())
        r_handler.iteration_reverse()
        self.base_config = r_handler.get_dist()
        setattr(applicationContext, "base_config", self.base_config)
