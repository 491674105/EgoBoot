NACOS_KEY = "nacos"
APP_NAME = {
    "key": "name",
    "default": "",
    "type": "string",
    "require": True,
    "description": ""
}
CONFIG = {
    "key": "config",
    "default": "",
    "type": "string",
    "require": True,
    "description": ""
}
GROUP = {
    "key": "group",
    "default": "DEFAULT_GROUP",
    "type": "string",
    "require": False,
    "description": ""
}
CLUSTER_NAME = {
    "key": "cluster_name",
    "default": "DEFAULT",
    "type": "string",
    "require": False,
    "description": ""
}
REPORTING_INTERVAL = {
    "key": "reporting_interval",
    "default": 5,
    "type": "int",
    "require": False,
    "description": ""
}
REFRESH_SUBSCRIBE = {
    "key": "refresh_subscribe",
    "default": 30,
    "type": "int",
    "require": False,
    "description": ""
}
PROFILE = {
    "key": "profile",
    "default": {},
    "type": "object",
    "require": True,
    "description": ""
}
ROUTES = {
    "key": "routes",
    "default": [],
    "type": "array",
    "require": False,
    "description": ""
}
