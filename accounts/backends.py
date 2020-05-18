from django.contrib.auth.backends import ModelBackend

from .models import User


class UsernameOrEmailBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None):
        if username is not None and password is not None:
            users = User.objects.filter(is_active=True, email=username)
            for user in users:
                if (user.check_password(password)
                        and self.user_can_authenticate(user)):
                    return user
        return None
