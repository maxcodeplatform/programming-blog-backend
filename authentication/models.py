from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from authentication.manager import CustomUserManager


class User(AbstractBaseUser):
    user_name = models.CharField(max_length=50, unique=True,)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_name'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return self.user_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
