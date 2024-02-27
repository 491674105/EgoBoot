"""
    json
"""
DEFAULT_JSON_ENCODER_KEY = "json_encoder"
# 默认JSON序列化处理器
DEFAULT_JSON_ENCODER_PACKAGE = "ego.utils.json.JSONEncoder"
JSON_ENCODER = {
    "key": "json_encoder",
    "default": DEFAULT_JSON_ENCODER_PACKAGE,
    "type": "string",
    "require": False,
    "description": ""
}