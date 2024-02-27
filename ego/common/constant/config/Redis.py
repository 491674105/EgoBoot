DEFAULT_REDIS_CONFIG_KEY = "redis"
NAME = {
    "key": "name",
    "default": "",
    "type": "string",
    "require": True,
    "description": ""
}
HOST = {
    "key": "host",
    "default": "",
    "type": "string",
    "require": True,
    "description": ""
}
PORT = {
    "key": "port",
    "default": -1,
    "type": "int",
    "require": True,
    "description": ""
}
PASSWORD = {
    "key": "password",
    "default": "",
    "type": "string",
    "require": False,
    "description": ""
}
DB = {
    "key": "db",
    "default": 0,
    "type": "int",
    "require": False,
    "description": ""
}
MODE = {
    "key": "mode",
    "default": 0,
    "type": "int",
    "require": False,
    "description": ""
}
MAX_ACTIVE = {
    "key": "max_active",
    "default": 16,
    "type": "int",
    "require": False,
    "description": ""
}
MAX_WAIT = {
    "key": "max_wait",
    "default": -1,
    "type": "int",
    "require": False,
    "description": ""
}
MAX_IDLE = {
    "key": "max_idle",
    "default": 8,
    "type": "int",
    "require": False,
    "description": ""
}
