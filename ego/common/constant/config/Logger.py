DEFAULT_LOG_CONFIG_KEY = "logger"
LEVEL = {
    "key": "level",
    "default": "DEBUG",
    "type": "string",
    "require": False,
    "description": ""
}
OUTPUT_FILE = {
    "key": "output_file",
    "default": "",
    "type": "string",
    "require": False,
    "description": ""
}
ENCODING = {
    "key": "encoding",
    "default": "UTF-8",
    "type": "string",
    "require": False,
    "description": ""
}
FORMAT = {
    "key": "fmt",
    "default": "%(asctime)s.%(msecs)03d %(levelname)s [%(service_port)s] [%(thread)d] [%(threadName)s] [%(uri)s] [%(relate_path)s.%(funcName)s:%(lineno)s] - %(message)s ",
    "type": "string",
    "require": False,
    "description": ""
}
DATE_FORMAT = {
    "key": "datefmt",
    "default": "%Y-%m-%d %H:%M:%S",
    "type": "string",
    "require": False,
    "description": ""
}
