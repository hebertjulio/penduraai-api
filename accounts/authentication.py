from rest_framework_simplejwt import authentication

from .models import Profile


class JWTAuthentication(authentication.JWTAuthentication):

    def authenticate(self, request):
        authenticate = super().authenticate(request)
        if not authenticate:
            return None
        user, validated_token = authenticate
        pk = JWTAuthentication.get_PIN(request.headers)
        profile = JWTAuthentication.get_profile(user, pk)
        if profile is not None:
            user.profile = profile
            return user, validated_token
        return None

    @staticmethod
    def get_PIN(headers):
        if 'Profile' not in headers:
            return None
        values = headers['Profile'].split()
        if len(values) != 2:
            return None
        name, value = values
        if not name.upper() == 'PK':
            return None
        try:
            value = int(value)
            return value
        except ValueError:
            return None

    @staticmethod
    def get_profile(user, pk):
        if pk is None:
            return None
        try:
            profile = user.profiles.get(pk=pk, is_active=True)
            return profile
        except Profile.DoesNotExist:
            return None
