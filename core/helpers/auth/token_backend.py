import jwt

from core.common.env_config_loader import Config
from core.exceptions.auth import TokenError, TokeDecodeError
from core.common.utils import aware_utcnow, datetime_to_epoch, datetime_from_epoch

config = Config.instance()


class BaseToken:
    token_type = None
    lifetime = None

    def __init__(self, token=None):
        if self.token_type in None and self.lifetime is None:
            raise TokenError("token_type and lifetime is required")
        self.token = token
        self.current_time = aware_utcnow()
        if token is not None:
            try:
                self.payload = self.decode(token)
            except TokeDecodeError:
                raise TokenError("Token is invalid or expired")
            self.check_exp()
        else:
            self.payload = {"type": self.token_type}
            self.set_exp(from_time=self.current_time, lifetime=self.lifetime)
            self.set_iat(at_time=self.current_time)

    @staticmethod
    def decode(token):
        try:
            return jwt.decode(token, config.JWT_SECRET, algorithms='HS256')
        except Exception:
            raise TokeDecodeError("Provided token is invalid or expired")

    def set_exp(self, claim="exp", from_time=None, lifetime=None):
        if from_time is None:
            from_time = self.current_time
        if lifetime is None:
            lifetime = self.lifetime
        self.payload[claim] = datetime_to_epoch(from_time + lifetime)

    def set_iat(self, claim="iat", at_time=None):
        if at_time is None:
            at_time = self.current_time
        self.payload[claim] = datetime_to_epoch(at_time)

    def encode(self):
        jwt_payload = self.payload.copy()
        token = jwt.encode(jwt_payload, config.JWT_SECRET, algorithm='HS256')
        return token

    @property
    def get_token(self):
        return self.encode()

    def check_exp(self, claim="exp", current_time=None):
        if current_time is None:
            current_time = self.current_time
        try:
            claim_value = self.payload[claim]
        except KeyError:
            raise TokenError("Token has no '{}' claim".format(claim))

        claim_time = datetime_from_epoch(claim_value)
        if claim_time <= current_time:
            raise TokenError("Token '{}' claim has expired".format(claim))
