from django.urls import path

app_name = "users"

urlpatterns = [
    path('', views.TokenLoginView.as_view(), name='login'),
    path('', views.RefreshTokenView.as_view(), name='refresh_token'),
    path('', views.TestView.as_view(), name='login'),
]