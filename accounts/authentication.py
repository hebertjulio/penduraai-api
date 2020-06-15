from rest_framework_simplejwt import authentication

from .models import Profile


class JWTAuthentication(authentication.JWTAuthentication):

    def authenticate(self, request):
        authenticate = super().authenticate(request)
        if authenticate:
            user, validated_token = authenticate
            pk = JWTAuthentication.get_PIN(request.headers)
            profile = JWTAuthentication.get_profile(user, pk)
            if profile is not None:
                user.profile = profile
                return user, validated_token
        return None

    @staticmethod
    def get_PIN(headers):
        if 'Profile' in headers:
            values = headers['Profile'].split()
            if len(values) == 2:
                name, value = values
                if name.upper() == 'PK':
                    try:
                        value = int(value)
                        return value
                    except ValueError:
                        pass
        return None

    @staticmethod
    def get_profile(user, pk):
        if pk is not None:
            try:
                profile = user.userprofiles.get(pk=pk, is_active=True)
                return profile
            except Profile.DoesNotExist:
                pass
        return None
