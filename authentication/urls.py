from django.urls import path

from authentication import views

app_name = "authentication"

urlpatterns = [
    path('login/', views.TokenLoginView.as_view(), name='login'),
    path('refresh-token/', views.RefreshTokenView.as_view(), name='refresh_token'),
    path('test/', views.TestView.as_view(), name='login'),
]