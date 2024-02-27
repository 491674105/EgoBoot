SQLALCHEMY_TRACK_MODIFICATIONS = {
    "key": "SQLALCHEMY_TRACK_MODIFICATIONS",
    "default": False,
    "type": "bool",
    "require": False,
    "description": ""
}
SQLALCHEMY_POOL_RECYCLE = {
    "key": "SQLALCHEMY_POOL_RECYCLE",
    "default": False,
    "type": "int",
    "require": False,
    "description": ""
}
SQLALCHEMY_DATABASE_URI = {
    "key": "SQLALCHEMY_DATABASE_URI",
    "default": "",
    "type": "string",
    "require": True,
    "description": ""
}
SQLALCHEMY_BINDS = {
    "key": "SQLALCHEMY_BINDS",
    "default": [],
    "type": "array",
    "require": False,
    "description": ""
}
