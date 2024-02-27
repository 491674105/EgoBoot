from locale import getdefaultlocale

"""
    system
"""
VERSION_ = "v3.0.0.0-20240101"

"""
    application
"""
MODULE_PATH_KEY = "module_path"
ENGINE_KEY = "engine"

"""
    server
"""
DEFAULT_HOSTING_KEY = "hosting"
DEFAULT_RUNNING_MODE_KEY = "running_mode"
DEFAULT_CORE_LOADED_KEY = "core_loaded"
DEFAULT_APP_LAUNCHED_KEY = "app_launched"
DEFAULT_LLM_KEY = "lazy_load_modules"
DEFAULT_LML_KEY = "lazy_module_launched"
DEFAULT_BRS_KEY = "blueprint_register_set"
DEFAULT_WBC_KEY = "wait_blueprint_create"
APPLICATION_KEY = "application"
APP_INFO_KEY = "info"
INFO_NAME = {
    "key": "name",
    "default": "",
    "type": "string",
    "require": False,
    "description": ""
}
INFO_VERSION = {
    "key": "version",
    "default": VERSION_,
    "type": "string",
    "require": False,
    "description": ""
}
APP_SERVER_KEY = "server"
APP_PORT = {
    "key": "port",
    "default": -1,
    "type": "int",
    "require": True,
    "description": ""
}

"""
    config_file
"""
BASE_CONFIG_VALID_KEY = "base_config_valid_key"
DEFAULT_CONFIG_FILE = "resources/bootstrap.yml"
ORIGINAL_KEY = "original"

"""
    encode
"""
DEFAULT_ENCODING = "UTF-8"
SYSTEM_ENCODING = getdefaultlocale()[1]

"""
  logger
"""
DEFAULT_OUTPUT_PATH_KEY = "output_file"
DEFAULT_LOGGER_PATH = "logs"
DEFAULT_LOGGER_FILE_SUFFIX = ".log"

"""
    datetime
"""
TIMEZONE = {
    "key": "timezone",
    "default": "",
    "type": "string",
    "require": False,
    "description": ""
}
