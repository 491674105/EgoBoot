"""
    flask
"""
DEFAULT_FLASK_CONFIG_KEY = "flask"
APPLICATION_KEY = "application"
APPLICATION_NAME = {
    "key": "name",
    "default": "",
    "type": "string",
    "require": True,
    "description": ""
}
ROOT_PATH = {
    "key": "root_path",
    "default": "/",
    "type": "string",
    "require": False,
    "description": ""
}
INTERCEPTOR_PATH = {
    "key": "interceptor_path",
    "default": "/",
    "type": "string",
    "require": False,
    "description": ""
}
FILTER_PATH = {
    "key": "filter_path",
    "default": "/",
    "type": "string",
    "require": False,
    "description": ""
}
ORIGINAL_KEY = "original"
ORIGINAL_JSON = {
    "key": "JSON_AS_ASCII",
    "default": False,
    "type": "bool",
    "require": False,
    "description": ""
}
CLOUD_KEY = "cloud"
