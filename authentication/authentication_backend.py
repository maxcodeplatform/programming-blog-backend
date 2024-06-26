from django.contrib.auth import get_user_model

from rest_framework import authentication, HTTP_HEADER_ENCODING
from rest_framework.exceptions import AuthenticationFailed

from config.constants.auth import AuthSetting
from core.exceptions.auth import TokenError, InvalidToken
from core.helpers.auth.token_backend import AccessToken


class CustomJWTAuthenticationBackend(authentication.BaseAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = get_user_model()

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        prefix, raw_token = self.get_auth_header_and_raw_token(header)
        if raw_token is None or prefix is None:
            return None
        try:
            validated_token = AccessToken(raw_token)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return self.get_user(validated_token), validated_token

    @staticmethod
    def get_header(request):
        header = request.META.get(AuthSetting.AUTH_HEADER_NAME.value)
        if isinstance(header, str):
            header = header.encode(HTTP_HEADER_ENCODING)
        return header

    @staticmethod
    def get_auth_header_and_raw_token(header):
        auth_header = header.split()
        if len(auth_header) == 0:
            return None, None

        if auth_header[0] != AuthSetting.AUTH_HEADER_TYPE.value.encode(HTTP_HEADER_ENCODING):
            return None, None

        if len(auth_header) != 2:
            raise AuthenticationFailed("Authorization header must contain two space-delimited values")
        return auth_header[0], auth_header[1]

    def get_user(self, validated_token):
        try:
            user_id = validated_token["id"]
        except KeyError:
            raise AuthenticationFailed("Token contained no recognizable user identification")

        try:
            user = self.user_model.objects.get(id=user_id)
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed("User not found")

        if not user.is_active:
            raise AuthenticationFailed("User is inactive")

        if not user.is_confirmed:
            raise AuthenticationFailed("account_not_confirm")

        if user.is_blocked:
            raise AuthenticationFailed("account_is_blocked")

        return user
