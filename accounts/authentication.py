from rest_framework_simplejwt import authentication

from .models import Profile


class JWTAuthentication(authentication.JWTAuthentication):

    def authenticate(self, request):
        authenticate = super().authenticate(request)
        if not authenticate:
            return None
        user, validated_token = authenticate
        pk = JWTAuthentication.get_profile_pk(request.headers)
        profile = JWTAuthentication.get_profile(user, pk)
        user.profile = profile
        return user, validated_token

    @staticmethod
    def get_profile_pk(headers):
        if 'Profile' not in headers:
            return None
        name, value = headers['Profile'].split()
        if not name.lower() == 'pk':
            return None
        try:
            pk = int(value)
            return pk
        except TypeError:
            pass
        return None

    @staticmethod
    def get_profile(user, pk):
        try:
            profile = user.accountable.get(pk=pk)
            return profile
        except Profile.DoesNotExist:
            pass
        return None
