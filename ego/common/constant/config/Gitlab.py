GITLAB_CONFIG_KEY = "gitlab"
GITLAB_NAME = {
    "key": "name",
    "default": "gitlab_main",
    "type": "string",
    "require": True,
    "description": ""
}
GITLAB_URL = {
    "key": "url",
    "default": "",
    "type": "string",
    "require": True,
    "description": ""
}
GITLAB_TOKEN = {
    "key": "token",
    "default": "",
    "type": "string",
    "require": False,
    "description": ""
}
GITLAB_SELF_HOSTED = {
    "key": "self_hosted",
    "default": True,
    "type": "bool",
    "require": True,
    "description": ""
}
GITLAB_TIMEOUT = {
    "key": "timeout",
    "default": 3,
    "type": "int",
    "require": False,
    "description": ""
}
GITLAB_SSL = {
    "key": "ssl",
    "default": False,
    "type": "bool",
    "require": False,
    "description": ""
}
