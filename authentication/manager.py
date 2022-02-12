from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, user_name, email, password=None):
        if not email:
            raise ValueError('User must have an email')

        if not user_name:
            raise ValueError('User Name must need to provide')

        email = self.normalize_email(email)
        user = self.model(
            user_name=user_name,
            email=email,
            is_active=True
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, email, password):
        user = self.create_user(user_name=user_name, email=email, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
