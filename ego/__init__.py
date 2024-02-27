from typing import Union

from logging import Logger

from ego.common.constant.config import Base


class ApplicationContext:
    def __init__(self, service_name=None):
        if service_name:
            self.service_name = service_name
        self.__bp_set = []

    @property
    def bp_set(self):
        return self.__bp_set

    @bp_set.setter
    def bp_set(self, bp):
        self.__bp_set.append(bp)

    def save_blueprint(self, bp_type, bp, cache_set_key=Base.DEFAULT_BRS_KEY):
        if not bp:
            bp_list = []
        elif isinstance(bp, list):
            bp_list = bp
        else:
            bp_list = [bp]

        if not hasattr(self, cache_set_key):
            setattr(self, cache_set_key, {bp_type: bp_list})
            return

        cache_set = getattr(self, cache_set_key)
        if bp_type not in cache_set:
            cache_set[bp_type] = bp_list
        else:
            cache_set[bp_type].extend(bp_list)
        setattr(self, cache_set_key, cache_set)

    def get_blueprint_set(self, cache_set_key=Base.DEFAULT_BRS_KEY):
        if not hasattr(self, cache_set_key):
            return {}
        return getattr(self, cache_set_key)

    def mark_blueprint(self, bp_type, delete=False, cache_set_key=Base.DEFAULT_WBC_KEY):
        cache_set = getattr(self, cache_set_key)
        if not delete:
            cache_set.add(bp_type)
        else:
            cache_set.discard(bp_type)
        setattr(self, cache_set_key, cache_set)

    def check_blueprint_finish(self, cache_set_key=Base.DEFAULT_WBC_KEY):
        if getattr(self, cache_set_key):
            return False
        else:
            return True


applicationContext = ApplicationContext()


class RouteContainer:
    def __init__(self):
        self.log: Union[Logger, None]
        self.service_instances = {}

    def add_instance(self, service_name, ip, port):
        unique_key = f"{ip}:{port}"
        if service_name in self.service_instances:
            if unique_key in self.service_instances[service_name]:
                return
            self.service_instances[service_name][unique_key] = {
                "ip": ip,
                "port": port
            }
        else:
            self.service_instances[service_name] = {
                unique_key: {
                    "ip": ip,
                    "port": port
                }
            }


routeContainer = RouteContainer()
