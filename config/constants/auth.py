from datetime import timedelta
from enum import Enum


class AuthSetting(Enum):
    AUTH_HEADER_NAME = "HTTP_AUTHORIZATION"
    AUTH_HEADER_TYPE = "Token"
    ACCESS_TOKEN_LIFETIME = timedelta(days=7)
    REFRESH_TOKEN_LIFETIME = timedelta(days=15)
