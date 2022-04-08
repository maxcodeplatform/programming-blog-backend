from core.helpers.auth.token_backend import AccessToken, RefreshToken
import os
import django


def run_code():
    class User:
        def __init__(self, _id):
            self.id = _id

    user = User(1)
    rtc = RefreshToken.login(user)
    print(rtc.access_token)
    print(rtc.get_token)


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'programming_blog.settings')
    django.setup()
    run_code()

