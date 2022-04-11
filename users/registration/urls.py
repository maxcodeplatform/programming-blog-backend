from django.urls import path

from users.registration import views


urlpatterns = [
    path("registration/", views.CreateUserView.as_view(), name="registration"),
    path("user-email-confirmation/", views.UserEmailConfirmationAPIView.as_view(), name="user_email_confirmation"),
]