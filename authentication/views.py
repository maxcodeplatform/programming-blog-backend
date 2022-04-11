from django.conf import settings

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from core.exceptions.auth import TokenError, InvalidToken
from config.constants.auth import AuthSetting

from authentication.serializers import AccessTokenSerializer, RefreshTokenSerializer


class TokenViewBase(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = None

    www_authenticate_realm = "api"

    def get_authenticate_header(self, request):
        return '{} realm="{}"'.format(
            AuthSetting.AUTH_HEADER_TYPE.value,
            self.www_authenticate_realm,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TokenLoginView(TokenViewBase):
    serializer_class = AccessTokenSerializer


class RefreshTokenView(TokenViewBase):
    serializer_class = RefreshTokenSerializer


class TestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        config = getattr(settings, "REST_FRAMEWORK", None)
        print(config)
        data = {
            "welcome": "you successfully logged in"
        }
        return Response(data, status=status.HTTP_200_OK)
