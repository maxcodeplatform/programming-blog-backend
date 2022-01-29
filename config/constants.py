from enum import Enum


class TYPE(Enum):
    Boolean = "Boolean"
    String = "String"
    Array = "Array"
    Number = "Number"
    Object = "Object"


class ConfigList(Enum):
    DEBUG = {"key": "DEBUG", "type": TYPE.Boolean}
    DATABASES = {"key": "DATABASES", "type": TYPE.Object}
    APP_SECRET = {"key": "APP_SECRET", "type": TYPE.String}
    ALLOWED_HOSTS = {"key": "ALLOWED_HOSTS", "type": TYPE.Array}
    ENV = {"key": "ENV", "type": TYPE.String}
