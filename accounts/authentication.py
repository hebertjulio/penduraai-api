from rest_framework_simplejwt import authentication

from .models import Profile


class JWTAuthentication(authentication.JWTAuthentication):

    def authenticate(self, request):
        authenticate = super().authenticate(request)
        if not authenticate:
            return None
        user, validated_token = authenticate
        pin = JWTAuthentication.get_PIN(request.headers)
        profile = JWTAuthentication.get_profile(user, pin)
        user.profile = profile
        return user, validated_token

    @staticmethod
    def get_PIN(headers):
        if 'Profile' not in headers:
            return None
        values = headers['Profile'].split()
        if len(values) != 2:
            return None
        name, value = values
        if not name.upper() == 'PIN':
            return None
        return value

    @staticmethod
    def get_profile(user, pin):
        if pin is not None:
            try:
                profile = user.profiles.get(pin=pin)
                return profile
            except Profile.DoesNotExist:
                pass
        return None
