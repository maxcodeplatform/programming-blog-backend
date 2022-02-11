from core.helpers.auth.token_backend import AccessToken, RefreshToken
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'programming_blog.settings')
django.setup()


def run_code():
    class User:
        def __init__(self, id):
            self.id = id

    user = User(1)
    rtc = RefreshToken.login(user)
    print(rtc.access_token)
    print(rtc.get_token)


if __name__ == "__main__":
    run_code()

