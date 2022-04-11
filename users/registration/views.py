from django.contrib.auth import get_user_model

from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from core.exceptions.auth import UserNotFound
from users.registration.serializers import UserRegistrationSerializer

User = get_user_model()


class CreateUserView(CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = UserRegistrationSerializer


class UserEmailConfirmationAPIView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get("user_id")
        if not user_id:
            return Response("`user_id` is require for email confirmation.", status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist as e:
            raise UserNotFound(e.args[0])
        user.is_confirmed = True
        user.save()
        return Response({"response": "User is confirmed successfully with user_id: {}".format(user_id)},
                        status=status.HTTP_200_OK)
