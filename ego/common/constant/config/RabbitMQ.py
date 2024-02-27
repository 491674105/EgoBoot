DEFAULT_RABBITMQ_CONFIG_KEY = "rabbitmq"
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
USERNAME = {
    "key": "username",
    "default": "",
    "type": "string",
    "require": False,
    "description": ""
}
PASSWORD = {
    "key": "password",
    "default": "",
    "type": "string",
    "require": False,
    "description": ""
}
VHOST = {
    "key": "vhost",
    "default": "",
    "type": "string",
    "require": True,
    "description": ""
}
