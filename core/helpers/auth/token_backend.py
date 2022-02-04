import jwt

from core.common.env_config_loader import Config
from core.exceptions.auth import TokenError, TokeDecodeError
from core.common.utils import aware_utcnow
config = Config.instance()


class BaseToken:
    token_type = None
    lifetime = None

    def __init__(self, token=None):
        if self.token_type in None and self.lifetime is None:
            raise TokenError("token_type and lifetime is required")
        self.token = token
        self.current_time = aware_utcnow
        if token is not None:
            try:
                self.payload = self.decode(token)
            except TokeDecodeError:
                raise TokenError("Token is invalid or expired")

    @staticmethod
    def decode(token):
        try:
            return jwt.decode(token, config.JWT_SECRET, algorithms='HS256')
        except Exception:
            raise TokeDecodeError("Provided token is invalid or expired")
